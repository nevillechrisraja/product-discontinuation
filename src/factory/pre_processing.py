class PreProcessing:
    """
    This class handles entire data preprocessing steps
    """
    def process(self, df):
        null_count, duplicates = self.check_null(df)

        return df

    def check_null(self, df):
        null_count = df.isnull().sum()
        duplicates = df.duplicated().isnull().sum()
        return null_count, duplicates
