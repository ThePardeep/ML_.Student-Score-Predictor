from flask import Flask, stream_template_string, request, jsonify, send_from_directory
from flask_cors import CORS
from src.utils.exception import CustomException
from pydantic import ValidationError
from src.pipeline.predict import StudentInput, PredictPipeline
import pandas as pd
from src.utils.logger import logging
import sys
import os

app = Flask(__name__, static_folder="ui/out", static_url_path="")
CORS(app)


@app.route("/")
def homePage(path="index.html"):
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        logging.info("Executing Predict Pipeline.")
        data = request.get_json()
        validate_data = StudentInput(**data)
        df = pd.DataFrame([validate_data.model_dump()])
        pp = PredictPipeline()

        predicted_score = pp.predict(df)
        return jsonify({"predicted_score": predicted_score[0]})
    except ValidationError as e:
        CustomException(e.errors(), sys)
        return (
            jsonify(
                {
                    "error": True,
                    "message": e.errors(
                        include_url=False, include_context=False, include_input=False
                    ),
                }
            ),
            400,
        )
    except Exception as e:
        CustomException(e, sys)
        return jsonify({"error": True, "message": e or "Something went wrong."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
