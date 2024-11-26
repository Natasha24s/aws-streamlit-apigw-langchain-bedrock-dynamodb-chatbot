# AWS Streamlit API Gateway LangChain Bedrock DynamoDB Chatbot

This repository contains the code and instructions for deploying a chatbot using AWS services including API Gateway, Lambda, Bedrock, and DynamoDB, with a Streamlit frontend.

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Deployment Steps](#deploymentsteps)
   - [Deploy CloudFormation Stack](#1-deploy-cloudformation-stack)
   - [Upload CSV Files to S3](#2-upload-csv-files-to-s3)
   - [Create Bedrock Knowledge Base](#3-create-bedrock-knowledge-base)
   - [Update Lambda Function](#4-update-lambda-function)
   - [Update Lambda Layer](#5-update-lambda-layer)
   - [Get API Gateway Invoke URL](#6-Get-API-Gateway-Invoke-URL)
   - [Deploy Streamlit Frontend](#7-Deploy-Streamlit-Frontend)
   - [Update API Gateway Endpoint](#8-Update-API-Gateway-Endpoint)
   - [Run the Streamlit App](#9-Run-the-Streamlit-App)



## Overview

This repository contains the code and instructions for deploying a chatbot using AWS services including API Gateway, Lambda, Bedrock, and DynamoDB, with a Streamlit frontend.

## Architecture

   ![Alt text](https://github.com/Natasha24s/aws-streamlit-apigw-langchain-bedrock-dynamodb-chatbot/blob/main/images/architecture.jpg)    

## Deployment Steps

### 1. Deploy CloudFormation Stack

Deploy the CloudFormation template to create the following resources:

- API Gateway
- Lambda Function
- DynamoDB Table
- S3 Bucket
- IAM Roles and Policies

### 2. Upload CSV Files to S3

Once the CloudFormation stack is deployed:

1. Open the S3 bucket created by the stack. You can find it in the resource section of your CloudFormation template.
2. Upload the CSV files that will be used for Retrieval Augmented Generation (RAG)

![Alt text](https://github.com/Natasha24s/aws-streamlit-apigw-langchain-bedrock-dynamodb-chatbot/blob/main/images/s3%20put%20object.png)


### 3. Create Bedrock Knowledge Base

Follow these steps to create and sync a knowledge base in Amazon Bedrock:

1. Navigate to the Bedrock console
2. Go to the "Knowledge bases" section
3. Click "Create knowledge base"
4. Configure the knowledge base settings
5. Add the S3 bucket as a data source

![Alt text](https://github.com/Natasha24s/aws-streamlit-apigw-langchain-bedrock-dynamodb-chatbot/blob/main/images/S3-data-source.png)

6. Start the sync process

![](https://github.com/Natasha24s/aws-streamlit-apigw-langchain-bedrock-dynamodb-chatbot/blob/main/images/sync%20data%20source.png)

7. Once synced, note down the knowledge base ID

![](https://github.com/Natasha24s/aws-streamlit-apigw-langchain-bedrock-dynamodb-chatbot/blob/main/images/Knowledge%20base%20ID.png)

### 4. Update Lambda Function

Update the following variables in the Lambda function code:

- `bedrock_model_id`: Find this in the Bedrock console under "Model access"
- `knowledge_base_id`: Use the ID noted from step 3
- `region_name`: Your AWS region

[Image Placeholder: Screenshot of updating Lambda function code]

### 5. Update Lambda Layer

Upload the provided layer.ZIP file as a new layer for the Lambda function.

### 6. Get API Gateway Invoke URL

Fetch the Invoke URL from the API Gateway console. You'll need this for the frontend integration.

![](https://github.com/Natasha24s/aws-streamlit-apigw-langchain-bedrock-dynamodb-chatbot/blob/main/images/api%20gateway%20invoke%20url.png)

### 7. Deploy Streamlit Frontend

Follow the instructions in `streamlit-apigateway-frontend.md` to deploy the Streamlit frontend.


### 8. Update API Gateway Endpoint

In the Streamlit app code, update the `config.py` file to use your own API Gateway endpoint URL you got in step 6.

![Alt text](https://github.com/Natasha24s/aws-streamlit-apigw-langchain-bedrock-dynamodb-chatbot/blob/main/images/config.py%20file.png)

### 9. Run the Streamlit App

To run the app locally:
   
`streamlit run src/app.py`

![Alt text](https://github.com/Natasha24s/aws-streamlit-apigw-langchain-bedrock-dynamodb-chatbot/blob/main/images/streamlit%20run%20command.png)

It will show up in your browser as shown below:

![](https://github.com/Natasha24s/aws-streamlit-apigw-langchain-bedrock-dynamodb-chatbot/blob/main/images/Streamlit.png)


