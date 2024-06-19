import logging
import os
import uuid
import variables

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger('main')
logger.setLevel("INFO")


class Utils:

    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            region_name='us-west-2',
            aws_access_key_id=variables.AWS_KEY,
            aws_secret_access_key=variables.AWS_SECRET_KEY,
            aws_session_token=variables.AWS_SESSION_TOKEN)
        self.bedrock_runtime_agent = boto3.client(
            service_name='bedrock-agent-runtime',
            region_name='us-west-2',
            aws_access_key_id=variables.AWS_SECRET_KEY,
            aws_secret_access_key=variables.AWS_SECRET_KEY,
            aws_session_token=variables.AWS_SECRET_KEY)
        self.bedrock_agent = boto3.client(
            service_name='bedrock-agent',
            region_name='us-west-2',
            aws_access_key_id=variables.AWS_SECRET_KEY,
            aws_secret_access_key=variables.AWS_SECRET_KEY,
            aws_session_token=variables.AWS_SECRET_KEY)

    def upload_file_to_s3(self, file_name, bucket):
        try:
            response = self.s3_client.upload_file(file_name, bucket, file_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload_files_to_s3(self, folder_path):
        for path in os.listdir(folder_path):
            self.upload_file_to_s3(f'{folder_path}/{path}', variables.BUCKET_NAME)

    def sync_knowledge_base(self):
        self.bedrock_agent.start_ingestion_job(
            dataSourceId=variables.DATASOURCE_ID,
            knowledgeBaseId=variables.KNOWLEDGE_BASE_ID)

        ingestion_job_list = self.bedrock_agent.list_ingestion_jobs(
            dataSourceId=variables.DATASOURCE_ID,
            knowledgeBaseId=variables.KNOWLEDGE_BASE_ID,
        )

        job_completed = False

        while not job_completed:
            job = ingestion_job_list['ingestionJobSummaries'][0]
            if job['status'] == 'COMPLETE':
                job_completed = True
            else:
                ingestion_job_list = self.bedrock_agent.list_ingestion_jobs(
                    dataSourceId=variables.DATASOURCE_ID,
                    knowledgeBaseId=variables.KNOWLEDGE_BASE_ID,
                )

        logger.info('Knowledge base has been synced!')

    def query_agent(self):
        session_id = uuid.uuid4().hex
        response = self.bedrock_runtime_agent.invoke_agent(
            agentId=variables.AGENT_ID,
            agentAliasId=variables.AGENT_ALIAS_ID,
            sessionId=session_id,
            inputText="What can you tell me about Everest",
        )
        completion = ""
        for event in response.get("completion"):
            chunk = event["chunk"]
            completion += chunk["bytes"].decode()
        print(completion)

    def clear_s3_data(self):
        self.s3_client.delete_object(variables.BUCKET_NAME, 'key')
        logger.info("S3 files deleted!")

    def clear_local_data(self, folder_path):
        for path in os.listdir(folder_path):
            os.remove(f'{folder_path}/{path}')
        logger.info("Local files cleared!")
