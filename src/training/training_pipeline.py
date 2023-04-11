import logging
from fetch.database_orm import DatabaseORM
from factory.preprocessor import Preprocessor
from training.modelling import Modelling


class TrainingPipeline:
    """
    In this class we will be performing the following operations.
    1. Extract input data from source
    2. Perform data pre-processing steps
    3. Perform ML modelling
    """

    def process(self, s3_client, db_user, db_password):
        database_orm_obj = DatabaseORM()
        df = database_orm_obj.extract_data(db_user, db_password)

        preprocessor_obj = Preprocessor()
        df = preprocessor_obj.process(df)

        modelling_obj = Modelling()
        modelling_obj.process(df, s3_client)
        logging.info("Training pipeline completed")