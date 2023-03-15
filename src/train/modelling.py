import logging
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier


class Modelling:
    def process(self, df):
        feature_imp_cols = ['HierarchyLevel2', 'CatEdition', 'ActualsPerWeek', 'Status_RO']
        target_col = 'DiscontinuedTF'
        x_train, x_test, y_train, y_test = self.dataset_split(feature_imp_cols, target_col, df)
        model = self.fit_model(x_train, y_train)


    def dataset_split(self, imp_cols, target_col, df):
        x = df[imp_cols]
        y = df[target_col]
        x_train, x_test, y_train, y_test = \
            train_test_split(x, y, random_state = 42, test_size = 0.20)
        print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)
        return x_train, x_test, y_train, y_test

    def fit_model(self, x_train, y_train):
        model = XGBClassifier(min_child_weight = 7, max_depth = 15, learning_rate = 0.2, gamma = 0.0, colsample_bytree = 0.7)
        model.fit(x_train, y_train)
        print(model)
        return model