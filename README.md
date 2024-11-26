# aws-streamlit-apigw-langchain-bedrock-dynamodb-chatbot

## Architecture

   ![Alt text](https://github.com/Natasha24s/aws-streamlit-apigw-langchain-bedrock-dynamodb-chatbot/blob/main/images/architecture.jpg)


   # AWS Streamlit API Gateway LangChain Bedrock DynamoDB Chatbot

This repository contains the code and instructions for deploying a chatbot using AWS services including API Gateway, Lambda, Bedrock, and DynamoDB, with a Streamlit frontend.

## Deployment Steps

### 1. Deploy CloudFormation Stack

Deploy the CloudFormation template to create the following resources:

- API Gateway
- Lambda Function
- DynamoDB Table
- S3 Bucket
- IAM Roles and Policies

[Image Placeholder: Screenshot of CloudFormation stack creation]

### 2. Upload CSV Files to S3

Once the CloudFormation stack is deployed:

1. Open the S3 bucket created by the stack
2. Upload the CSV files that will be used for Retrieval Augmented Generation (RAG)

[Image Placeholder: Screenshot of uploading CSV files to S3]

### 3. Create Bedrock Knowledge Base

Follow these steps to create and sync a knowledge base in Amazon Bedrock:

1. Navigate to the Bedrock console
2. Go to the "Knowledge bases" section
3. Click "Create knowledge base"
4. Configure the knowledge base settings
5. Add the S3 bucket as a data source
6. Start the sync process
7. Once synced, note down the knowledge base ID

[Image Placeholder: Screenshot of Bedrock knowledge base creation and sync]

### 4. Update Lambda Function

Update the following variables in the Lambda function code:

- `bedrock_model_id`: Find this in the Bedrock console under "Model access"
- `knowledge_base_id`: Use the ID noted from step 3
- `region_name`: Your AWS region

[Image Placeholder: Screenshot of updating Lambda function code]

### 5. Update Lambda Layer

Upload the provided layer.ZIP file as a new layer for the Lambda function.

[Image Placeholder: Screenshot of updating Lambda layer]

### 6. Get API Gateway Invoke URL

Fetch the Invoke URL from the API Gateway console. You'll need this for the frontend integration.

[Image Placeholder: Screenshot of API Gateway Invoke URL]

### 7. Deploy Streamlit Frontend

Follow the instructions in `streamlit-apigateway-frontend.md` to deploy the Streamlit frontend.

[Image Placeholder: Screenshot of Streamlit deployment steps]

### 8. Update API Gateway Endpoint

In the Streamlit app code, update the `config.py` file to ue your own API Gateway endpoint URL you got in step 6.

### 9. Run the Streamlit App

To run the app locally:
   
`streamlit run src/app.py`

!(https://github.com/Natasha24s/aws-streamlit-apigw-langchain-bedrock-dynamodb-chatbot/blob/main/images/Streamlit.png)


