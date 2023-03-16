import logging
import pandas as pd


class ExtractData:
    """
    This class handles the data extraction
    """

    def extract(self) -> pd.DataFrame:
        """
        This method fetches data from the source
        """
        catalogue_df = pd.read_csv("src/fetch/CatalogueDiscontinuation.csv")
        product_df = pd.read_csv('src/fetch/ProductDetails.csv')
        df = pd.merge(product_df, catalogue_df, how = 'inner', on = 'ProductKey')
        df = df.sample(frac = 0.01)
        logging.info("Extract completed successfully")
        return df