import logging
from fetch.extract_data import ExtractData

def main():
    """
    In this method we will be performing the following operations.
    1. Extract input data from source
    """
    extract_data_obj = ExtractData()
    df = extract_data_obj.extract()
    logging.info("Execution completed successfully")

if __name__ == "__main__":
    main()