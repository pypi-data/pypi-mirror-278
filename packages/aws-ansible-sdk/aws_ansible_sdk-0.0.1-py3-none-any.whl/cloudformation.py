import boto3
import os
from dotenv import load_dotenv

load_dotenv(".env")

# retrieve AWS credentials from env variables
aws_access_key = os.environ.get("AWS_ACCESS_KEY")
aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

github_token = os.environ.get("GITHUB_TOKEN")

# create a session and CloudFormation client using the credentials
session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)
cloudformation = session.client('cloudformation')

# create a new stack
response = cloudformation.create_stack(
    StackName='my-stack',
    TemplateURL='https://s3.amazonaws.com/my-bucket/my-template.yml',
    Parameters=[
        {
            'ParameterKey': 'parameter1',
            'ParameterValue': 'value1'
        }
    ]
)
print(response)

# delete a stack
response = cloudformation.delete_stack(
    StackName='my-stack'
)
print(response)
