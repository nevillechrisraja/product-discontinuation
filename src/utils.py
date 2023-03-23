import logging
import boto3


def s3_connection(api_key, api_secret):
    """
    Setting up access to S3
    """

    client = boto3.client("s3", aws_access_key_id = api_key,
        aws_secret_access_key = api_secret)
    logging.info("S3 connection successful")
    return client