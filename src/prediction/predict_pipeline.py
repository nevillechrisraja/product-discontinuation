import logging
from configparser import ConfigParser
from fetch.extract_data import ExtractData
from factory.pre_processing import PreProcessing
import ast
import numpy as np
import joblib
from io import BytesIO
import pandas as pd
from datetime import datetime

config = ConfigParser()
file = "config.ini"
config.read(file)

feature_imp_cols = config["hyperparams"]["feature_imp_cols"]
model_dir = config["model_path"]["model_dir"]
filename = config["model_path"]["filename"]
s3_bucket = config["s3_storage"]["s3_bucket"]
s3_key = config["s3_storage"]["s3_key"]


class PredictPipeline:
    """
    In this class we will be performing the following operations.
    1. Extract input data from source
    2. Perform data pre-processing steps
    3. Load saved model from S3
    4. Perform prediction
    """


    def process(self, s3_client, db_user, db_password) -> np.array:
        extract_data_obj = ExtractData()
        df = extract_data_obj.extract_data(db_user, db_password)
        pre_processing_obj = PreProcessing()
        df = pre_processing_obj.process(df)
        model = self.read_joblib(s3_client)
        df_results = self.predict(df, feature_imp_cols, model)
        extract_data_obj.push_data(db_user, db_password, df_results)
        logging.info("Prediction pipeline completed")


    def read_joblib(self, s3_client):
        """
        This method reads a joblib file from a S3 bucket
        """
        # Path is an s3 bucket
        with BytesIO() as f:
            s3_client.download_fileobj(Bucket = s3_bucket, Key = s3_key, Fileobj = f)
            f.seek(0)
            model_file = joblib.load(f)
        logging.info("Prediction for new data points completed successfully")
        return model_file


    def predict(self, df, imp_cols, model) -> pd.DataFrame:
        """
        This method performs prediction on the new data points
        """
        cols = ['id', 'discontinued', 'date_created']
        imp_cols = ast.literal_eval(imp_cols)
        df_results = model.predict(df[imp_cols])
        df_results = pd.DataFrame(df_results)
        df_results['date_created'] = pd.to_datetime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        df_results['id'] = df['id']
        df_results.columns = ['discontinued', 'date_created', 'id']
        df_results['discontinued'] = df_results['discontinued'].map({1: True, 0: False})
        logging.info("Prediction for new data points completed successfully")
        return df_results[cols]
