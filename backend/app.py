# Import the necessary libraries
import numpy as np
import joblib               # For loading the serialized model
import pandas as pd         # For data manipulation
from flask import Flask, request, jsonify   # For creating the Flask API

# Initialize the Flask application
superkart_api = Flask("SuperKart Sales Predictor")

# Load the trained machine learning pipeline (preprocessing + model)
model = joblib.load("superkart_model.joblib")

# The exact set of features the model was trained on
FEATURES = [
    "Product_Weight", "Product_Sugar_Content", "Product_Allocated_Area",
    "Product_MRP", "Store_Size", "Store_Location_City_Type", "Store_Type",
    "Product_Id_char", "Store_Age_Years", "Product_Type_Category",
]

# Home route (GET request)
@superkart_api.get('/')
def home():
    return "Welcome to the SuperKart Sales Prediction API!"

# Endpoint for single (online) prediction (POST request)
@superkart_api.post('/v1/predict')
def predict_sales():
    # Read the JSON payload from the request body
    product_data = request.get_json()

    # Keep only the expected features, in the expected order
    sample = {feature: product_data[feature] for feature in FEATURES}

    # Convert to a single-row DataFrame the pipeline can consume
    input_data = pd.DataFrame([sample])

    # Predict and convert the numpy value to a native Python float for JSON
    prediction = round(float(model.predict(input_data)[0]), 2)

    return jsonify({"Predicted Product Store Sales Total": prediction})

# Endpoint for batch prediction (POST request)
@superkart_api.post('/v1/predictbatch')
def predict_sales_batch():
    # Read the uploaded CSV file into a DataFrame
    file = request.files['file']
    input_data = pd.read_csv(file)

    # Predict for every row
    predictions = [round(float(p), 2) for p in model.predict(input_data).tolist()]

    # Return a dict of {row index: predicted sales}
    output_dict = dict(zip(input_data.index.astype(str), predictions))
    return output_dict

# Run the app (used for local testing; in Docker we run it via gunicorn)
if __name__ == '__main__':
    superkart_api.run(debug=True)
