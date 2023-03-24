import logging
import pandas as pd
import redshift_connector
from configparser import ConfigParser

config = ConfigParser()
file = "config.ini"
config.read(file)

db_host = config["redshift_connection"]["host"]
db_port = int(config["redshift_connection"]["port"])
db = config["redshift_connection"]["database"]


class ExtractData:
    """
    This class handles the data extraction
    """


    def extract(self, db_user, db_password) -> pd.DataFrame:
        """
        This method fetches data from the source
        """
        conn = redshift_connector.connect(
            host = db_host,
            port = db_port,
            database = db,
            user = db_user,
            password = db_password
        )
        # Create a Cursor object
        cursor = conn.cursor()

        # Query and receive result set
        cursor.execute\
        (
            """
            select 
                pd.ProductKey, pd.Supplier, pd.HierarchyLevel1, pd.HierarchyLevel2, pd.DIorDOM, 
                pd.Seasonal, cd.CatEdition, cd.SpringSummer, cd.WeeksOut, cd.Status, 
                cd.SalePriceIncVAT, cd.ForecastPerWeek, cd.ActualsPerWeek, cd.DiscontinuedTF
            from 
                productdetail pd 
                join cataloguediscontinued cd 
                on pd.productkey = cd.productkey
            """
        )
        df: pd.DataFrame = cursor.fetch_dataframe()
        df = df.sample(frac=0.01)
        logging.info("Extract completed successfully")
        return df
