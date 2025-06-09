from pydantic import BaseModel, confloat
from typing import Literal
from src.utils.exception import CustomException
from src.utils.common import load_object
import os
import sys

class StudentInput(BaseModel):
    gender: Literal["male", "female"]
    race_ethnicity: Literal["group A", "group B", "group C", "group D", "group E"]
    parental_level_of_education: Literal[
        "high school",
        "some high school",
        "associate's degree",
        "some college",
        "bachelor's degree",
        "master's degree",
    ]
    lunch: Literal["standard", "free/reduced"]
    test_preparation_course: Literal["none", "completed"]
    reading_score: confloat(ge=0, le=100)
    writing_score: confloat(ge=0, le=100)


class PredictPipeline:

    def __init__(self):
        pass

    def predict(self, features):
        try:
            model_path = os.path.join("artifacts", "model.pkl")
            preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            data_scaled = preprocessor.transform(features)
            predicted_score = model.predict(data_scaled)
            return predicted_score

        except Exception as e:
            raise CustomException(e, sys)
