import logging
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import os
import pickle
import ast


from configparser import ConfigParser

config = ConfigParser()
file = "config.ini"
config.read(file)

feature_imp_cols = config["hyperparams"]["feature_imp_cols"]
model_dir = config["model_path"]["model_dir"]
filename = config["model_path"]["filename"]

class Modelling:
    """
    In this class we will be performing the following operations.
    1. Perform train test split
    2. Fit data to the model
    3. Save the model for future predictions
    """
    def process(self, df):
        target_col = 'DiscontinuedTF'
        x_train, x_test, y_train, y_test = self.dataset_split(feature_imp_cols, target_col, df)
        model = self.fit_model(x_train, y_train)
        self.save_model(model)
        logging.info("Modelling completed successfully")

    def dataset_split(self, imp_cols, target_col, df):
        imp_cols = ast.literal_eval(imp_cols)
        x = df[imp_cols]
        y = df[target_col]
        x_train, x_test, y_train, y_test = \
            train_test_split(x, y, random_state = 42, test_size = 0.20)
        logging.info("Train test split completed successfully")
        return x_train, x_test, y_train, y_test

    def fit_model(self, x_train, y_train):
        model = XGBClassifier(min_child_weight = 7, max_depth = 15, learning_rate = 0.2, gamma = 0.0, colsample_bytree = 0.7)
        model.fit(x_train, y_train)
        logging.info("Model fit completed successfully")
        return model

    def save_model(self, model):
        path = os.path.join(model_dir)
        with open(path + filename + '.sav', 'wb') as f:
            pickle.dump(model, f)
        logging.info("Model saved successfully")
