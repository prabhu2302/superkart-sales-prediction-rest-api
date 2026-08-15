import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend. Because both containers share the same Docker
# network, the frontend can reach the backend using its container name "backend".
BACKEND_URL = "http://backend:7860"

st.title("SuperKart Sales Prediction")

# ---------------- Online (single) Prediction ----------------
st.subheader("Online Prediction")

product_weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
product_sugar_content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
product_allocated_area = st.number_input("Product Allocated Area (ratio)", min_value=0.0, max_value=1.0, value=0.027, format="%.3f")
product_mrp = st.number_input("Product MRP", min_value=0.0, value=117.08)
store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
store_location_city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
product_id_char = st.selectbox("Product Id Category (FD=Food, DR=Drinks, NC=Non-Consumable)", ["FD", "DR", "NC"])
store_age_years = st.number_input("Store Age (Years)", min_value=0, value=16)
product_type_category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

# Assemble the user input into a single-row DataFrame
input_data = pd.DataFrame([{
    "Product_Weight": product_weight,
    "Product_Sugar_Content": product_sugar_content,
    "Product_Allocated_Area": product_allocated_area,
    "Product_MRP": product_mrp,
    "Store_Size": store_size,
    "Store_Location_City_Type": store_location_city_type,
    "Store_Type": store_type,
    "Product_Id_char": product_id_char,
    "Store_Age_Years": store_age_years,
    "Product_Type_Category": product_type_category,
}])

if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=input_data.to_dict(orient="records")[0])
    if response.status_code == 200:
        prediction = response.json()["Predicted Product Store Sales Total"]
        st.success(f"Predicted Product Store Sales Total: {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# ---------------- Batch Prediction ----------------
st.subheader("Batch Prediction")
uploaded_file = st.file_uploader("Upload a CSV file for batch prediction", type=["csv"])

if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file})
        if response.status_code == 200:
            st.success("Batch predictions completed!")
            st.write(response.json())
        else:
            st.error("Unable to connect to the prediction API.")
