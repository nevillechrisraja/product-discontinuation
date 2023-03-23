import logging
import argparse
from training.train_pipeline import TrainPipeline
from prediction.predict_pipeline import PredictPipeline

logging.basicConfig(filename = "log.txt", level = logging.DEBUG,
                    format = "%(asctime)s %(message)s", datefmt = "%m/%d/%Y %I:%M:%S %p")

def main(run_type):
    """
    In this method we will be performing the following operations.
    1. Perform training
    2. Perform prediction
    """
    logging.info("Execution started successfully")
    if run_type:
        train_pipeline_obj = TrainPipeline()
        train_pipeline_obj.process()
    predict_pipeline_obj = PredictPipeline()
    predict_pipeline_obj.process()

    logging.info("Execution completed successfully")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", dest = "run_type", type = bool, help = "execution flow type")
    args = parser.parse_args()
    main(run_type = args.run_type)