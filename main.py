import streamlit as st
import pickle
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# Paths (make sure model.pickle and params.pickle sit in the same folder
# as this script, or adjust the subfolder names accordingly)
# ──────────────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pickle"
PARAMS_PATH= BASE_DIR / "params.pickle"

# ──────────────────────────────────────────────────────────────────────────────
# Load your trained model and parameter metadata
# ──────────────────────────────────────────────────────────────────────────────
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(PARAMS_PATH, "rb") as f:
    params = pickle.load(f)

# ──────────────────────────────────────────────────────────────────────────────
# Streamlit page setup
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bengaluru House Price Prediction",
    page_icon=":house:"
)

st.title("Bengaluru House Price Prediction")
st.subheader("Predict the price of a house in Bengaluru using Machine Learning")

# ──────────────────────────────────────────────────────────────────────────────
# User inputs
# ──────────────────────────────────────────────────────────────────────────────
total_sq_feet   = st.number_input(
    "Total Square Feet",
    placeholder="Enter the total square feet area of the house",
    min_value=300,
    max_value=100000
)
number_bathrooms= st.number_input(
    "Number of Bathrooms",
    placeholder="Enter the number of bathrooms in the house",
    min_value=1,
    max_value=20
)
number_bedrooms = st.number_input(
    "Number of Bedrooms",
    placeholder="Enter the number of bedrooms in the house",
    min_value=1,
    max_value=20
)
location        = st.selectbox(
    "Choose the location of the house",
    params["columns"]
)

# ──────────────────────────────────────────────────────────────────────────────
# Prediction logic
# ──────────────────────────────────────────────────────────────────────────────
if st.button("Predict", type="primary"):
    # build feature vector
    n_cols = len(params["columns"])
    prefix = params["prefix"]
    features = [0] * (n_cols + prefix)
    features[0] = total_sq_feet
    features[1] = number_bathrooms
    features[2] = number_bedrooms
    idx = prefix + params["columns"].index(location)
    features[idx] = 1

    # model output is in lakhs if you trained it that way,
    # so multiply by 100_000 to get rupees
    price = model.predict([features])[0] * 100_000

    if price <= 0:
        st.error(
            "The location you have chosen does not have any houses "
            "with the entered features"
        )
    else:
        # simple formatting: commas + two decimal places + ₹ symbol
        price_str = f"₹{price:,.2f}"
        st.success(f"The predicted price of the house is {price_str}")
