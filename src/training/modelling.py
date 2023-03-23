import logging
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import ast
from io import BytesIO
import joblib
from configparser import ConfigParser

config = ConfigParser()
file = "config.ini"
config.read(file)

feature_imp_cols = config["hyperparams"]["feature_imp_cols"]
model_dir = config["model_path"]["model_dir"]
filename = config["model_path"]["filename"]
s3_bucket = config["s3_storage"]["s3_bucket"]
s3_key = config["s3_storage"]["s3_key"]

class Modelling:
    """
    In this class we will be performing the following operations.
    1. Perform train test split
    2. Fit data to the model
    3. Save the model for future predictions
    """
    def process(self, df, s3_client):
        target_col = 'DiscontinuedTF'
        x_train, x_test, y_train, y_test = self.dataset_split(feature_imp_cols, target_col, df)
        model = self.fit_model(x_train, y_train)
        self.write_joblib(model, s3_client)
        logging.info("Modelling completed successfully")

    def dataset_split(self, imp_cols, target_col, df):
        """
        This method performs the train test split
        """
        imp_cols = ast.literal_eval(imp_cols)
        x = df[imp_cols]
        y = df[target_col]
        x_train, x_test, y_train, y_test = \
            train_test_split(x, y, random_state = 42, test_size = 0.20)
        logging.info("Train test split completed successfully")
        return x_train, x_test, y_train, y_test

    def fit_model(self, x_train, y_train):
        """
        In this method we fit the dataset to the ML algorithm
        """
        model = XGBClassifier(min_child_weight = 7, max_depth = 15, learning_rate = 0.2, gamma = 0.0, colsample_bytree = 0.7)
        model.fit(x_train, y_train)
        logging.info("Model fit completed successfully")
        return model

    def write_joblib(self, model, s3_client):
        """
        This method writes a joblib file to a S3 bucket
        """
        with BytesIO() as f:
            joblib.dump(model, f)
            f.seek(0)
            s3_client.upload_fileobj(Bucket = s3_bucket, Key = s3_key, Fileobj = f)
