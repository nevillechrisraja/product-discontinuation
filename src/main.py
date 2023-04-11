import logging
import argparse
from dotenv import load_dotenv
import os
from utils import s3_connection
from training.training_pipeline import TrainingPipeline
from prediction.prediction_pipeline import PredictionPipeline

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

logging.basicConfig(filename = "log.txt", level = logging.DEBUG,
                    format = "%(asctime)s %(message)s", datefmt = "%m/%d/%Y %I:%M:%S %p")

def main(run_type):
    """
    In this method we will be performing the following operations.
    1. Perform training
    2. Perform prediction
    """
    logging.info("Execution started successfully")
    s3_client = s3_connection(api_key, api_secret)
    if run_type:
        training_pipeline_obj = TrainingPipeline()
        training_pipeline_obj.process(s3_client, db_user, db_password)
    prediction_pipeline_obj = PredictionPipeline()
    prediction_pipeline_obj.process(s3_client, db_user, db_password)

    logging.info("Execution completed successfully")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", dest = "run_type", type = bool, help = "execution flow type")
    args = parser.parse_args()
    main(run_type = args.run_type)