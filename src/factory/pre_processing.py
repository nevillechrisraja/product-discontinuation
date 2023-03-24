import logging
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")


class PreProcessing:
    """
    This class handles entire data preprocessing steps
    """


    def process(self, df) -> pd.DataFrame:
        null_count, duplicates = self.check_null(df)
        categorical_cols = ['seasonal', 'springsummer', 'discontinued']
        df = self.encode_binary_features(categorical_cols, df)
        categorical_cols = ['diordom', 'status']
        df = self.encode_multi_features(categorical_cols, df)
        logging.info("Preprocessing steps completed successfully")
        return df


    def check_null(self, df):
        """
        This method checks for null values and duplicates in the input dataset
        """
        df.reset_index(inplace = True, drop = True)
        null_count = df.isnull().sum()
        duplicates = df.duplicated().isnull().sum()
        logging.info("Null and duplicate check completed successfully")
        return null_count, duplicates


    def encode_binary_features(self, cols, df) -> pd.DataFrame:
        """
        This method encodes the binary categorical features to numerical features
        """
        for i in cols:
            df[i] = df[i].map({True: 1, False: 0})
        logging.info("Encoding binary categorical features completed successfully")
        return df


    def encode_multi_features(self, cols, df) -> pd.DataFrame:
        """
        This method encodes the multi categorical features to numerical features
        """
        ohe = OneHotEncoder(sparse = False, handle_unknown = 'ignore')
        for i in cols:
            feature_array = ohe.fit_transform(df[[i]])
            feature_labels = np.array(ohe.categories_).ravel()
            df_encoded = pd.DataFrame(feature_array, columns = feature_labels)
            first_feature = ohe.categories_[0][0]
            df_encoded.drop([first_feature], axis = 1, inplace = True)
            df_encoded = df_encoded.add_prefix(i+ '_')
            df = pd.concat([df, df_encoded], axis = 1)
        df.drop(cols, axis = 1, inplace = True)
        logging.info("Encoding multi categorical features completed successfully")
        return df