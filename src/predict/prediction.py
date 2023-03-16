import logging
from configparser import ConfigParser
import os
import pickle


config = ConfigParser()
file = "config.ini"
config.read(file)

feature_imp_cols = config["hyperparams"]["feature_imp_cols"]
model_dir = config["model_path"]["model_dir"]
filename = config["model_path"]["filename"]


class Prediction:
    def process(self, df):
        model = self.load_model()

    def load_model(self):
        path = os.path.join(model_dir)
        with open(path + '/' + filename + '.sav', 'rb') as f:
            model = pickle.load(f)
            return model