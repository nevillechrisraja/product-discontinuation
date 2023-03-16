import logging
from fetch.extract_data import ExtractData
from factory.pre_processing import PreProcessing
from train.modelling import Modelling

logging.basicConfig(filename = "log.txt", level = logging.DEBUG,
                    format = "%(asctime)s %(message)s", datefmt = "%m/%d/%Y %I:%M:%S %p")

def main():
    """
    In this method we will be performing the following operations.
    1. Extract input data from source
    2. Perform data pre-processing steps
    3. Perform ML modelling
    """
    logging.info("Execution started successfully")

    extract_data_obj = ExtractData()
    df = extract_data_obj.extract()

    pre_processing_obj = PreProcessing()
    df = pre_processing_obj.process(df.head())

    modelling_obj = Modelling()
    modelling_obj.process(df)

    logging.info("Execution completed successfully")

if __name__ == "__main__":
    main()