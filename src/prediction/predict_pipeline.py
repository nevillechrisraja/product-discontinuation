import logging
from configparser import ConfigParser
import os
from fetch.extract_data import ExtractData
from factory.pre_processing import PreProcessing
import pickle
import ast
import numpy as np

config = ConfigParser()
file = "config.ini"
config.read(file)

feature_imp_cols = config["hyperparams"]["feature_imp_cols"]
model_dir = config["model_path"]["model_dir"]
filename = config["model_path"]["filename"]


class PredictPipeline:
    """
    In this class we will be performing the following operations.
    1. Extract input data from source
    2. Perform data pre-processing steps
    3. Load saved model
    4. Perform prediction
    """


    def process(self) -> np.array:
        extract_data_obj = ExtractData()
        df = extract_data_obj.extract()
        pre_processing_obj = PreProcessing()
        df = pre_processing_obj.process(df.head())
        model = self.load_model()
        df_results = self.predict(df, feature_imp_cols, model)
        logging.info("Prediction pipeline completed")
        return df_results


    def load_model(self):
        path = os.path.join(model_dir)
        with open(path + '/' + filename + '.sav', 'rb') as f:
            model = pickle.load(f)
        logging.info("Saved model loaded successfully")
        return model


    def predict(self, df, imp_cols, model) -> np.array:
        imp_cols = ast.literal_eval(imp_cols)
        df_results = model.predict(df[imp_cols])
        logging.info("Prediction for new data points completed successfully")
        return df_results
