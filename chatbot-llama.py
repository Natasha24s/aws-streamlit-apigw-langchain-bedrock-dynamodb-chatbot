import json
import os
import boto3
import time
from typing import Any, List, Mapping, Optional, Iterator
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.prompts import PromptTemplate
import logging
from langchain.schema import AIMessage, BaseMessage, ChatResult, HumanMessage, SystemMessage, ChatGeneration
from langchain_community.retrievers import AmazonKnowledgeBasesRetriever
from langchain.chat_models.base import BaseChatModel
from pydantic import Field
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
import uuid

session_id = str(uuid.uuid4())

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
bedrock_runtime = boto3.client("bedrock-runtime")
dynamodb = boto3.client('dynamodb')

class BedrockLlama3ChatModel(BaseChatModel):
    model_id: str = Field(..., description="The Bedrock model ID")
    client: Any = Field(..., description="The Bedrock client")
    max_tokens: int = Field(512, description="Maximum number of tokens to generate")
    temperature: float = Field(0.7, description="Temperature for response generation")
    top_p: float = Field(0.9, description="Top p for response generation")

    class Config:
        arbitrary_types_allowed = True

    @property
    def _llm_type(self) -> str:
        return "bedrock-llama3-chat"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[str]:
        prompt = self._convert_messages_to_prompt(messages)

        body = json.dumps({
            "prompt": prompt,
            "max_gen_len": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p
        })

        response_stream = self.client.invoke_model_with_response_stream(
            modelId=self.model_id,
            contentType="application/json",
            accept="application/json",
            body=body
        )

        return self._process_stream(response_stream)

    def _process_stream(self, response_stream: Iterator[Any]) -> Iterator[str]:
        for event in response_stream['body']:
            if 'chunk' in event:
                chunk = json.loads(event['chunk']['bytes'].decode())
                if 'generation' in chunk:
                    yield chunk['generation']

    def _convert_messages_to_prompt(self, messages: List[BaseMessage]) -> str:
        prompt = ""
        for message in messages:
            if isinstance(message, SystemMessage):
                prompt += f"[INST] <<SYS>>\n{message.content}\n<</SYS>>\n\n"
            elif isinstance(message, HumanMessage):
                prompt += f"{message.content} [/INST]\n"
            elif isinstance(message, AIMessage):
                prompt += f"{message.content}\n\n"
        return prompt

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model_id": self.model_id}

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event, indent=2)}")

    # Get environment variables
    bedrock_model_id = "us.meta.llama3-1-70b-instruct-v1:0"
    knowledge_base_id = os.environ['KNOWLEDGE_BASE_ID']

    logger.info(f"Using Bedrock Model ID: {bedrock_model_id}")
    logger.info(f"Using Knowledge Base ID: {knowledge_base_id}")

    # Define system message
    system_message = """
    You are an AI assistant for product information. Be concise in your responses. Always be polite and professional.
    Never provide information about competitors' products.
    Do not discuss availability. If asked, say this information changes frequently and encourage users to visit our website or contact customer service for the most up-to-date information.
    Always respect user privacy and do not ask for or store personal information.
    """

    # Initialize BedrockLlama3ChatModel
    llm = BedrockLlama3ChatModel(
        model_id=bedrock_model_id, 
        client=bedrock_runtime,
        max_tokens=512,
        temperature=0.7,
        top_p=0.9
    )

    try:
        # Get user input from the event
        user_input = event.get('query')

        logger.info(f"User input: {user_input}")
        logger.info(f"Session ID: {session_id}")

        if not user_input:
            logger.error("No query provided in the event")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No query provided in the event'})
            }

        # Initialize DynamoDBChatMessageHistory
        message_history = DynamoDBChatMessageHistory(
            table_name="ConversationHistory",
            session_id=session_id,
        )

        # Retrieve chat history
        chat_history = message_history.messages

        # Add the new user message to the history
        message_history.add_user_message(user_input)

        # Initialize AmazonKnowledgeBasesRetriever
        retriever = AmazonKnowledgeBasesRetriever(
            knowledge_base_id=knowledge_base_id,
            retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 4}},
            region_name="us-east-2",
            return_source_documents=True
        )

        # Retrieve relevant documents
        docs = retriever.get_relevant_documents(user_input)
        context = "\n".join([f"Source {i+1}: {doc.page_content}" for i, doc in enumerate(docs)])

        # Create a custom prompt template
        prompt_template = """
        Use the following context and chat history to answer the question. Your response should be a concise summary of the information found in the search results, with key points or features listed in bullet points if appropriate.

        Context:
        {context}

        Chat History:
        {chat_history}

        Question: {question}

        Generate a response in the following format:
        Based on the search results, here's the information about [topic of the question]:
        - [Key point or feature 1]
        - [Key point or feature 2]
        - [Key point or feature 3]
        [Additional information if necessary]

        Answer:
        """

        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "chat_history", "question"])

        # Generate response
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=prompt.format(
                context=context, 
                chat_history="\n".join([f"{m.type}: {m.content}" for m in chat_history]), 
                question=user_input
            ))
        ]

        # Generate the full response
        full_response = "".join(llm._generate(messages))

        # Add the AI's response to the chat history
        message_history.add_ai_message(full_response)

        return {
            'statusCode': 200,
            'query': user_input,
            'generated_response': full_response
        }

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'An unexpected error occurred.',
                'details': str(e)
            })
        }
