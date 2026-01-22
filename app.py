import streamlit as st
import pickle
import pandas as pd

# Load model
with open("house_price_model.pkl", "rb") as file:
    model = pickle.load(file)

st.set_page_config(page_title="House Price Prediction", layout="centered")

st.title("🏠 House Price Prediction App")
st.write("Enter house details to predict the price")

# Inputs
area = st.number_input("Area (sq ft)", min_value=500, max_value=10000, step=100)
bedrooms = st.number_input("Bedrooms", 1, 10)
bathrooms = st.number_input("Bathrooms", 1, 10)
stories = st.number_input("Stories", 1, 5)
parking = st.number_input("Parking spaces", 0, 5)

mainroad = st.selectbox("Main Road", ["yes", "no"])
guestroom = st.selectbox("Guest Room", ["yes", "no"])
basement = st.selectbox("Basement", ["yes", "no"])
airconditioning = st.selectbox("Air Conditioning", ["yes", "no"])

furnishingstatus = st.selectbox(
    "Furnishing Status",
    ["furnished", "semi-furnished", "unfurnished"]
)

# Encode binary
mainroad = 1 if mainroad == "yes" else 0
guestroom = 1 if guestroom == "yes" else 0
basement = 1 if basement == "yes" else 0
airconditioning = 1 if airconditioning == "yes" else 0

# Encode furnishing status (drop_first=True logic)
furn_semi = 1 if furnishingstatus == "semi-furnished" else 0
furn_un = 1 if furnishingstatus == "unfurnished" else 0

# Input dataframe (MATCH TRAINING FEATURES)
input_data = pd.DataFrame({
    'area': [area],
    'bedrooms': [bedrooms],
    'bathrooms': [bathrooms],
    'stories': [stories],
    'mainroad': [mainroad],
    'guestroom': [guestroom],
    'basement': [basement],
    'airconditioning': [airconditioning],
    'parking': [parking],
    'furnishingstatus_semi-furnished': [furn_semi],
    'furnishingstatus_unfurnished': [furn_un]
})

# Ensure correct feature order
input_data = input_data[model.feature_names_in_]

# Prediction
if st.button("Predict Price"):
    prediction = model.predict(input_data)[0]
    st.success(f"💰 Estimated House Price: ₹ {int(prediction):,}")
