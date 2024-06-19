# Documentation
You can run tests by running `main.py` where it'll save the data found into the local directory. The commented out functions will help with cleaning up the data as well sync the Bedrock knowledge base and allowing you to query the bot from your code

# Resources
* https://repost.aws/questions/QUyEzvSFF2Q4iGm8M7mCSe8A/amazon-bedrock-knowledgebase-does-knowledge-base-support-json-files-in-s3
* https://medium.com/@mahmood1/slack-ai-bot-with-aws-bedrock-f95e7997a666
* https://medium.com/@18bhavyasharma/exploring-the-power-of-amazon-bedrock-services-on-aws-cloud-with-cohere-models-03a0bcdd2077#:~:text=With%20Amazon%20Bedrock%2C%20developers%20can,privacy%2C%20and%20responsible%20AI%20practices.

# Things that were done:

### Test which models could be found
    bedrock = boto3.client(
        service_name='bedrock',
        region_name='us-west-2',
        aws_access_key_id=AWS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        aws_session_token=AWS_SESSION_TOKEN)

    response = bedrock.list_foundation_models(byProvider='anthropic')

    for summary in response['modelSummaries']:
        print(summary['modelId'])

### Test if we can query the models from our application
    bedrock = boto3.client(
        # service_name='bedrock-runtime',
        region_name='us-west-2',
        aws_access_key_id=AWS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        aws_session_token=AWS_SESSION_TOKEN)
    
    body = json.dumps({
        "max_tokens": 256,
        "messages": [{"role": "user", "content": "What are you?"}],
        "anthropic_version": "bedrock-2023-05-31"
    })

    response = bedrock.invoke_model(body=body, modelId="anthropic.claude-3-haiku-20240307-v1:0")

    response_body = json.loads(response.get("body").read())
    print(response_body.get("content"))

### Test if agent created through UI exists
    bedrock = boto3.client(
        service_name='bedrock-agent',
        region_name='us-west-2',
        aws_access_key_id=AWS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        aws_session_token=AWS_SESSION_TOKEN)
    try:
        response = bedrock.get_agent(agentId='SP4L03I7QL')
        agent = response["agent"]
    except ClientError as e:
        raise e
    else:
        print(agent)
