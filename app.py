from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging
import traceback

import pandas as pd
import joblib

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

# Load the pre-trained model and scaler
try:
    clf = joblib.load("random_forest_model.pkl")  # Correct model filename
    scaler = joblib.load("scaler.joblib")         # Pre-fitted scaler file
    LOG.info("Model and scaler loaded successfully.")
except Exception as e:
    LOG.error("Error loading model or scaler: %s", str(e))
    LOG.error("Exception traceback: %s", traceback.format_exc())

@app.route("/")
def home():
    return "<h3>Random Forest Regressor Prediction API</h3>"

@app.route("/predict", methods=["POST"])
def predict():
    """
    Perform a RandomForest prediction with the following input format:
    {
      "CRIM": { "0": 5.82115 },
      "ZN": { "0": 0.0 },
      "INDUS": { "0": 18.1 },
      "CHAS": { "0": 0.0 },
      "NX": { "0": 0.713 },
      "RM": { "0": 6.513 },
      "AGE": { "0": 89.9 },
      "DIS": { "0": 2.8016 },
      "RAD": { "0": 24.0 },
      "TAX": { "0": 666.0 },
      "PTRATIO": { "0": 20.2 },
      "B": { "0": 393.82 },
      "LSTAT": { "0": 10.29 }
    }
    """
    try:
        # Receive and log the JSON payload
        json_payload = request.json
        LOG.info("Received JSON payload: %s", json_payload)
        
        # Convert payload to DataFrame
        inference_payload = pd.DataFrame(json_payload)
        LOG.info("Inference payload DataFrame: \n%s", inference_payload)

        # Scale the payload using the pre-fitted scaler
        scaled_payload = scaler.transform(inference_payload)
        
        # Perform prediction
        prediction = clf.predict(scaled_payload).tolist()
        LOG.info("Prediction: %s", prediction)
        
        # Return the prediction
        return jsonify({"prediction": prediction})
    
    except Exception as e:
        LOG.error("Error during prediction: %s", str(e))
        LOG.error("Exception traceback: %s", traceback.format_exc())
        return jsonify({"error": "Prediction failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
