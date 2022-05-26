from requests_aws4auth import AWS4Auth
import boto3
import os

# TODO Move this to a config file
role_arn = os.environ['ARN_ROLE']
region = 'us-east-1'
service = 'es'

# Gets temporary AWS credentials 
def get_aws_auth(role_arn=role_arn, region=region, service=service):
    sts_client = boto3.client('sts')
    assumed_role = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="AWSElasticSession"
    )
    credentials = assumed_role['Credentials']
    aws_auth = AWS4Auth(credentials['AccessKeyId'], credentials['SecretAccessKey'], region, service, session_token=credentials['SessionToken'])
    return aws_auth
