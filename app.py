import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("bike_sales_model.pkl")

# Page title
st.title("Bike Sales Profit Prediction")

st.write("Enter customer and product details")

# User Inputs
customer_age = st.number_input("Customer Age", min_value=10, max_value=100, value=25)

customer_gender = st.selectbox(
    "Customer Gender",
    ["M", "F"]
)

country = st.selectbox(
    "Country",
    ["United States", "United Kingdom", "Germany", "France", "Canada", "Australia"]
)

product_category = st.selectbox(
    "Product Category",
    ["Accessories", "Bikes", "Clothing"]
)

order_quantity = st.number_input(
    "Order Quantity",
    min_value=1,
    value=1
)

unit_cost = st.number_input(
    "Unit Cost",
    min_value=0.0,
    value=100.0
)

unit_price = st.number_input(
    "Unit Price",
    min_value=0.0,
    value=150.0
)

# Prediction button
if st.button("Predict Profit"):

    # Create dataframe
    input_data = pd.DataFrame({
        'Customer_Age': [customer_age],
        'Customer_Gender': [customer_gender],
        'Country': [country],
        'Product_Category': [product_category],
        'Order_Quantity': [order_quantity],
        'Unit_Cost': [unit_cost],
        'Unit_Price': [unit_price]
    })

    # Predict
    prediction = model.predict(input_data)

    # Show result
    st.success(f"Predicted Profit: ${prediction[0]:.2f}")
