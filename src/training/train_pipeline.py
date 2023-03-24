import logging
from fetch.extract_data import ExtractData
from factory.pre_processing import PreProcessing
from training.modelling import Modelling


class TrainPipeline:
    """
    In this class we will be performing the following operations.
    1. Extract input data from source
    2. Perform data pre-processing steps
    3. Perform ML modelling
    """

    def process(self, s3_client, db_user, db_password):
        extract_data_obj = ExtractData()
        df = extract_data_obj.extract_data(db_user, db_password)

        pre_processing_obj = PreProcessing()
        df = pre_processing_obj.process(df)

        modelling_obj = Modelling()
        modelling_obj.process(df, s3_client)
        logging.info("Training pipeline completed")