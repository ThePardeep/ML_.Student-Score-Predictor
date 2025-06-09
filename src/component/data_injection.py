from dataclasses import dataclass
from src.utils.logger import logging
from src.utils.exception import CustomException
import sys
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from src.component.data_transformer import DataTransformation
from src.component.model_train import ModelTrainer


@dataclass
class DataInjectionConfig:
    artifacts_folder_path: str = os.path.join("artifacts")
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "raw.csv")


class DataInjection:

    def __init__(self):
        self.data_injection_config = DataInjectionConfig()

    def initDataInjection(self):
        logging.info("Executing initDataInjection.")
        try:
            df = pd.read_csv("notebook/data/stud.csv")
            logging.info("DataFrame read successfully.")

            os.makedirs(
                os.path.join(self.data_injection_config.artifacts_folder_path),
                exist_ok=True,
            )

            df.to_csv(
                self.data_injection_config.raw_data_path, index=False, header=True
            )

            train_set, test_set = train_test_split(df, test_size=0.4, random_state=42)

            train_set.to_csv(
                self.data_injection_config.train_data_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_injection_config.test_data_path, index=False, header=True
            )

            logging.info("Data Injection Complete.")

            return {
                "train_date_file_path": self.data_injection_config.train_data_path,
                "test_date_file_path": self.data_injection_config.test_data_path,
            }
        except Exception as e:
            CustomException(e, sys)


if __name__ == "__main__":

    data_injection = DataInjection()
    file_paths = data_injection.initDataInjection()

    data_transformation = DataTransformation()

    train_arr, test_arr, _ = data_transformation.initDataTransformation(
        file_paths["train_date_file_path"], file_paths["test_date_file_path"]
    )

    modelTrainer = ModelTrainer()
    print(modelTrainer.initiate_model_trainer(train_arr, test_arr))

