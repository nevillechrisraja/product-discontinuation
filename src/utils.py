import logging
import boto3
import redshift_connector
from configparser import ConfigParser
import pandas as pd

config = ConfigParser()
file = "config.ini"
config.read(file)

db_host = config["redshift_connection"]["host"]
db_port = int(config["redshift_connection"]["port"])

def s3_connection(api_key, api_secret):
    """
    Setting up access to S3
    """

    client = boto3.client("s3", aws_access_key_id = api_key,
        aws_secret_access_key = api_secret)
    logging.info("S3 connection successful")
    return client


def db_connection(db_user, db_password, db_name) -> pd.DataFrame:
    """
    This method fetches data from the source
    """
    conn = redshift_connector.connect(
        host = db_host,
        port = db_port,
        database = db_name,
        user = db_user,
        password = db_password
    )
    logging.info("DB connection successful")
    return conn
