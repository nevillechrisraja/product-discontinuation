import logging
import boto3

def s3_connection(api_key, api_secret):
    connection = boto3.resource(
        service_name='s3',
        region_name='us-east-2',
        aws_access_key_id=api_key,
        aws_secret_access_key=api_secret
    )
    logging.info("S3 connection successful")
    return connection