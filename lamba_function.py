import uuid
import json
import boto3
import urllib3
import os
import utils

SLACK_URL = 'https://slack.com/api/chat.postMessage'
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
AWS_KEY = os.environ.get('AWS_KEY')
AWS_USER_SECRET_KEY = os.environ.get('AWS_USER_SECRET_KEY')
AGENT_ALIAS_ID = os.environ.get('AGENT_ALIAS_ID')
AGENT_ID = os.environ.get('AGENT_ID')
AWS_SESSION_ACCESS_TOKEN = os.environ.get('AWS_SESSION_ACCESS_TOKEN')

http = urllib3.PoolManager()


def call_bedrock(question):
    bedrock = boto3.client(
        service_name='bedrock-agent-runtime',
        region_name='us-west-2',
        aws_access_key_id=AWS_KEY,
        aws_secret_access_key=AWS_USER_SECRET_KEY,
        aws_session_token=AWS_SESSION_ACCESS_TOKEN)

    session_id = uuid.uuid4().hex
    response = bedrock.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId=session_id,
        inputText=f"\n\n{question}\n\nAssistant:",
    )

    completion = ""

    for event in response.get("completion"):
        chunk = event["chunk"]
        completion += chunk["bytes"].decode()

    return completion


def lambda_handler(event, context):
    if 'x-slack-retry-num' in event['headers']:
        slk_retry = event['headers']['x-slack-retry-num']
        if int(slk_retry) > 1:
            print(f'Retry: {slk_retry}')
            return 200
    else:
        slack_body = json.loads(event['body'])
        print(f'Slack event:{event}')

        slack_text = slack_body.get('event').get('text')
        slack_user = slack_body.get('event').get('user')
        # Ignore messages from the bot itself
        if slack_user == 'INSERT BOT ID':
            return 200
        channel = slack_body.get('event').get('channel')

        msg = call_bedrock(slack_text.replace('<@U075N2V1SSE>', '').lower())

        data = {'channel': channel, 'text': f"<@{slack_user}> {msg}"}
        print(f'Data: {data}')

        headers = {
            'Authorization': f'Bearer {SLACK_TOKEN}',
            'Content-Type': 'application/json',
        }

        response = http.request('POST', SLACK_URL, headers=headers, body=json.dumps(data))

        return {
            'statusCode': 200,
            'body': json.dumps({'msg': "message recevied"})
        }
