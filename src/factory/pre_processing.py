class PreProcessing:
    """
    This class handles entire data preprocessing steps
    """
    def process(self, df):
        null_count, duplicates = self.check_null(df)
        categorical_cols = ['Seasonal', 'SpringSummer', 'DiscontinuedTF']
        df = self.binary_encoding(categorical_cols, df)
        return df


    def check_null(self, df):
        null_count = df.isnull().sum()
        duplicates = df.duplicated().isnull().sum()
        return null_count, duplicates


    def binary_encoding(self, categorical_cols, df):
        for i in categorical_cols:
            df[i] = df[i].map({True: 1, False: 0})
        return df