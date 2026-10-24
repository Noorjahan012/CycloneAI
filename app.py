

import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(
    page_title="CycloneAI",
    page_icon="🌪️",
    layout="wide"
)

st.title("🌪️ CycloneAI")
st.subheader("AI-Based Cyclone Prediction and Impact Assessment")

st.write(
    "A student prototype for cyclone intensity estimation, "
    "geographic risk assessment, and evacuation support."
)

st.warning(
    "This is an experimental prototype, not an official forecasting "
    "system. Do not use its predictions for real evacuation decisions."
)

MODEL_PATH = "models/intensity_model.pkl"

if not os.path.exists(MODEL_PATH):
    st.error("Trained model not found. Run: python train_model.py")
    st.stop()

saved_model = joblib.load(MODEL_PATH)
model = saved_model["model"]
features = saved_model["features"]

st.success("AI model loaded successfully!")

st.markdown("---")
st.header("Cyclone Intensity Estimation")

col1, col2 = st.columns(2)

with col1:
    latitude = st.number_input(
        "Current latitude",
        min_value=-90.0,
        max_value=90.0,
        value=15.0
    )

    longitude = st.number_input(
        "Current longitude",
        min_value=-180.0,
        max_value=180.0,
        value=82.0
    )

with col2:
    wind_speed = st.number_input(
        "Current wind speed (knots)",
        min_value=0.0,
        max_value=250.0,
        value=50.0
    )

    month = st.selectbox(
        "Observation month",
        options=list(range(1, 13)),
        index=9
    )

if st.button("Estimate Next-Observation Wind Speed"):
    input_data = pd.DataFrame(
        [[latitude, longitude, wind_speed, month]],
        columns=features
    )

    prediction = float(model.predict(input_data)[0])

    # Display the model's numerical estimate without hiding
    # unexpected predictions by silently changing the result.
    st.subheader("Model Estimate")

    st.metric(
        "Estimated wind speed at next observation",
        f"{prediction:.2f} knots",
        help="This is a model estimate, not an official forecast."
    )

    st.write(f"Equivalent speed: **{prediction * 1.852:.2f} km/h**")

    st.caption(
        "The model was trained to predict the next recorded observation. "
        "It does not specify a fixed forecast horizon."
    )

st.markdown("---")
st.header("Project Modules")

st.markdown("""
- **Intensity estimation:** Uses the trained machine-learning model.
- **Track visualization:** Planned interactive map of cyclone positions.
- **Impact assessment:** Planned geographic exposure analysis.
- **Evacuation support:** Planned decision-support module using verified data.
""")

st.info(
    "The intensity model is a baseline. Track prediction, validated hazard "
    "mapping, and evacuation-support features require further development."
)
