from dataclasses import dataclass
from src.utils.exception import CustomException
from src.utils.common import getNumericalAndCategoricalFeatures, save_object
import sys
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from src.utils.logger import logging
import numpy as np
import os


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation:

    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def getColumnTransformer(self, numerical_features, categorical_features):
        try:
            logging.info("Executing getColumnTransformer.")

            numerical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            )

            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                ]
            )

            logging.info(f"Categorical columns: {categorical_features}")
            logging.info(f"Numerical columns: {numerical_features}")

            preprocessor = ColumnTransformer(
                [
                    ("numerical_pipeline", numerical_pipeline, numerical_features),
                    (
                        "categorical_pipeline",
                        categorical_pipeline,
                        categorical_features,
                    ),
                ]
            )

            logging.info("getColumnTransformer execution complete.")

            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)

    def initDataTransformation(self, train_date_filepath, test_date_filepath):

        try:
            logging.info("Executing initDataTransformation")
            train_data_frame = pd.read_csv(train_date_filepath)
            test_data_frame = pd.read_csv(train_date_filepath)
            numerical_features, categorical_features = (
                getNumericalAndCategoricalFeatures(train_data_frame)
            )
            numerical_features.remove("math_score")  # Removing dependent feature.
            target_feature = "math_score"

            preprocessing = self.getColumnTransformer(
                numerical_features, categorical_features
            )

            # TRAIN
            input_features_train_df = train_data_frame.drop(
                columns=[target_feature], axis=1
            )
            target_features_train_df = train_data_frame[target_feature]


            # TEST
            input_features_test_df = test_data_frame.drop(
                columns=[target_feature], axis=1
            )
            target_features_test_df = test_data_frame[target_feature]

            input_features_train_arr = preprocessing.fit_transform(
                input_features_train_df
            )
            input_features_test_arr = preprocessing.transform(
                input_features_test_df
            )

            train_arr = np.c_[
                input_features_train_arr, np.array(target_features_train_df)
            ]

            test_arr = np.c_[input_features_test_arr, np.array(target_features_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(
                self.data_transformation_config.preprocessor_obj_file_path,
                preprocessing,
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)
