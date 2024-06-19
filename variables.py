import os

AWS_KEY = os.environ.get('AWS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN')

AGENT_ID = os.environ.get('AGENT_ID')
AGENT_ALIAS_ID = os.environ.get('AGENT_ALIAS_ID')
DATASOURCE_ID = os.environ.get('DATA_SOURCE_ID')
KNOWLEDGE_BASE_ID = os.environ.get('KNOWLEDGE_BASE_ID')
BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

ATLASSIAN_ACCESS_KEY = os.environ.get('ATLASSIAN_ACCESS_KEY')
ATLASSIAN_DOMAIN = os.environ.get('ATLASSIAN_DOMAIN')
ATLASSIAN_EMAIL = os.environ.get('ATLASSIAN_EMAIL')