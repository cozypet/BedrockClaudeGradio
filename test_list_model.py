import boto3 
bedrock = boto3.client(service_name='bedrock')

models = bedrock.list_foundation_models()

print(models)