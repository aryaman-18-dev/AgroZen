"""Streamlit UI for the fertilizer recommendation model."""
from pathlib import Path
import pandas as pd
import streamlit as st
from src.model import predict_fertilizer, load_error

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "fertilizer_dataset.csv"

st.set_page_config(page_title="Fertilizer Recommendation System", page_icon="🌿", layout="centered")
st.title("🌾 Fertilizer Recommendation System")
st.write("Enter observed conditions to get a preliminary model suggestion.")
st.info("This prototype uses only 99 training rows. Confirm fertilizer needs with a recent soil test and local agronomy advice.")

if load_error:
    st.error(load_error)
    st.code(f'python "{ROOT / "src" / "train.py"}"', language="powershell")
    st.stop()

try:
    dataset = pd.read_csv(DATA_PATH)
    soil_options = sorted(dataset["Soil Type"].dropna().astype(str).unique())
    crop_options = sorted(dataset["Crop Type"].dropna().astype(str).unique())
except Exception as exc:
    st.error(f"Could not load the fertilizer dataset choices: {exc}")
    st.stop()

with st.form("fertilizer_form"):
    st.subheader("Environmental conditions")
    c1, c2, c3 = st.columns(3)
    temperature = c1.number_input("Temperature (°C)", min_value=0.0, max_value=60.0, value=25.0)
    humidity = c2.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0)
    moisture = c3.number_input("Moisture (%)", min_value=0.0, max_value=100.0, value=50.0)
    st.subheader("Soil and crop")
    soil_type = st.selectbox("Soil type", soil_options)
    crop_type = st.selectbox("Crop type", crop_options)
    c4, c5, c6 = st.columns(3)
    nitrogen = c4.number_input("Nitrogen (N)", min_value=0, max_value=140, value=60)
    potassium = c5.number_input("Potassium (K)", min_value=0, max_value=140, value=50)
    phosphorous = c6.number_input("Phosphorus (P)", min_value=0, max_value=140, value=40)
    submitted = st.form_submit_button("Recommend fertilizer")

if submitted:
    try:
        result = predict_fertilizer(
            temperature, humidity, moisture, soil_type, crop_type,
            nitrogen, potassium, phosphorous,
        )
        if result["recommendation"] is None:
            st.warning(result["message"])
        else:
            st.success(f"Preliminary suggestion: {result['recommendation']}")
            st.caption(f"Raw model score: {result['score']:.1%} (not calibrated). {result['message']}")
    except Exception as exc:
        st.error(f"Could not generate a recommendation: {exc}")
