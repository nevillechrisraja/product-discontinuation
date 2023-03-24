import logging
import pandas as pd
from utils import db_connection
from configparser import ConfigParser

config = ConfigParser()
file = "config.ini"
config.read(file)

table_target = config["redshift_connection"]["table_target"]


class ExtractData:
    """
    This class handles
    1. Data extraction from source db
    2. Push prediction results to target db
    """


    def extract_data(self, db_user, db_password) -> pd.DataFrame:
        """
        This method fetches data from the source
        """
        db_name = config["redshift_connection"]["database_source"]
        conn = db_connection(db_user, db_password, db_name)
        cursor = conn.cursor()

        cursor.execute\
        (
            """
            select 
                pd.ProductKey, pd.Supplier, pd.HierarchyLevel1, pd.HierarchyLevel2, pd.DIorDOM, 
                pd.Seasonal, cd.Id, cd.CatEdition, cd.SpringSummer, cd.WeeksOut, cd.Status, 
                cd.SalePriceIncVat, cd.ForecastPerWeek, cd.ActualsPerWeek, cd.Discontinued
            from 
                ProductDetail pd
                join CatalogueDiscontinued cd
                on pd.ProductKey = cd.ProductKey
            """
        )
        df: pd.DataFrame = cursor.fetch_dataframe()
        #df = df.sample(frac=0.01)
        cursor.close()
        logging.info("Extract completed successfully")
        return df


    def push_data(self, db_user, db_password, df_results):
        """
        This method pushes prediction results to a table
        """
        db_name = config["redshift_connection"]["database_target"]
        conn = db_connection(db_user, db_password, db_name)
        cursor = conn.cursor()
        table_target = 'catalogue_discontinued'

        sql = """select (1) from information_schema.tables where table_name = '""" + table_target+ """'"""
        cursor.execute(sql)
        if cursor.fetchone() is None:
            cursor.execute("""create table """ + table_target+ """ (id INTEGER, discontinued BOOLEAN, date_created TIMESTAMP)""")

        cursor.write_dataframe(df_results, table_target)
        cursor.close()
        conn.commit()
        conn.close()
        logging.info("Pushing predictions to table completed successfully")