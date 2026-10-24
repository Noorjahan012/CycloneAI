import streamlit as st
import folium
from streamlit_folium import st_folium


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Impact Assessment | CycloneAI",
    page_icon="🌪️",
    layout="wide"
)

st.title("🌪️ CycloneAI - Impact Assessment")

st.write(
    "Explore potential wind-related impacts using an illustrative "
    "risk assessment based on cyclone wind speed."
)

st.warning(
    "DEMONSTRATION ONLY: This module does not issue official warnings "
    "or predict actual damage, flooding, storm surge, or evacuation needs."
)


# --------------------------------------------------
# WIND SPEED INPUT
# --------------------------------------------------

st.subheader("1. Enter Cyclone Information")

col1, col2 = st.columns(2)

with col1:
    wind_speed = st.number_input(
        "Wind speed (knots)",
        min_value=0.0,
        max_value=250.0,
        value=50.0,
        step=5.0,
        help="Enter a measured or model-estimated wind speed."
    )

with col2:
    location_name = st.text_input(
        "Location name (optional)",
        placeholder="Example: Coastal area"
    )


# --------------------------------------------------
# CONVERT WIND SPEED
# --------------------------------------------------

wind_kmh = wind_speed * 1.852
wind_mph = wind_speed * 1.15078


# --------------------------------------------------
# ILLUSTRATIVE RISK CATEGORIES
# --------------------------------------------------

def assess_wind_risk(speed):

    if speed < 34:
        return (
            "Lower wind-speed category",
            "Limited wind-related impacts may occur.",
            "green"
        )

    elif speed < 64:
        return (
            "Tropical-storm-force wind range",
            "Potential for damaging winds, depending on exposure "
            "and local conditions.",
            "orange"
        )

    elif speed < 83:
        return (
            "Hurricane-force wind range",
            "Potential for serious wind damage. Actual impacts "
            "depend on structures, exposure, and other conditions.",
            "red"
        )

    elif speed < 96:
        return (
            "Very intense hurricane-force wind range",
            "Potential for severe wind damage and dangerous conditions.",
            "red"
        )

    else:
        return (
            "Extremely intense wind range",
            "Potential for catastrophic wind damage. Follow official "
            "warnings and emergency instructions.",
            "darkred"
        )


risk_level, impact_summary, risk_color = assess_wind_risk(wind_speed)


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

st.subheader("2. Wind-Based Impact Assessment")

metric1, metric2, metric3 = st.columns(3)

metric1.metric(
    "Wind speed",
    f"{wind_speed:.1f} knots"
)

metric2.metric(
    "Wind speed",
    f"{wind_kmh:.1f} km/h"
)

metric3.metric(
    "Wind speed",
    f"{wind_mph:.1f} mph"
)

st.markdown("### Illustrative Wind-Risk Category")

if risk_color == "green":
    st.success(f"**{risk_level}**")

elif risk_color == "orange":
    st.warning(f"**{risk_level}**")

else:
    st.error(f"**{risk_level}**")

st.write(impact_summary)

if location_name.strip():
    st.write(f"**Location entered:** {location_name.strip()}")


# --------------------------------------------------
# IMPACT FACTORS
# --------------------------------------------------

st.subheader("3. Factors That Affect Actual Impacts")

st.write(
    "Wind speed alone cannot determine the actual impact of a cyclone. "
    "A more complete assessment would need reliable information about "
    "the following factors."
)

factors = {
    "Population exposure": (
        "The number of people in potentially affected areas."
    ),
    "Infrastructure vulnerability": (
        "Building strength, roads, bridges, electricity, and communications."
    ),
    "Rainfall and flooding": (
        "Observed or forecast rainfall, drainage, and river conditions."
    ),
    "Storm surge": (
        "Coastal water-level changes and local coastal geography."
    ),
    "Forecast uncertainty": (
        "Uncertainty in cyclone intensity, movement, and timing."
    )
}

for factor, explanation in factors.items():
    with st.expander(factor):
        st.write(explanation)


# --------------------------------------------------
# ILLUSTRATIVE WIND-RISK SCALE
# --------------------------------------------------

st.subheader("4. Illustrative Wind-Speed Scale")

st.write(
    "The following thresholds are simplified demonstration categories. "
    "They are not a complete official cyclone classification system."
)

risk_data = [
    ("Below 34 knots", "Below 62.97 km/h", "Lower wind-speed category"),
    ("34–63 knots", "62.97–116.68 km/h", "Tropical-storm-force range"),
    ("64–82 knots", "118.53–151.86 km/h", "Hurricane-force range"),
    ("83–95 knots", "153.72–175.94 km/h", "Very intense wind range"),
    ("96 knots and above", "177.79 km/h and above", "Extremely intense wind range")
]

st.table(
    {
        "Wind speed": [row[0] for row in risk_data],
        "Approximate equivalent": [row[1] for row in risk_data],
        "Illustrative category": [row[2] for row in risk_data]
    }
)


# --------------------------------------------------
# SAFETY GUIDANCE
# --------------------------------------------------

st.subheader("5. Cyclone Safety Guidance")

st.markdown(
    """
    - Monitor official weather bulletins and local emergency alerts.
    - Follow evacuation orders issued by the relevant authorities.
    - Prepare drinking water, essential medicines, a torch, batteries,
      and important documents.
    - Stay away from windows during dangerous winds.
    - Avoid flooded roads and never walk or drive through floodwater.
    - Do not go outside to observe a cyclone.
    - Keep mobile phones charged and maintain contact with family.
    """
)

st.info(
    "The wind-risk category shown above must not be used to decide "
    "whether to evacuate. Follow official instructions for your area."
)


# --------------------------------------------------
# OFFICIAL INFORMATION
# --------------------------------------------------

st.subheader("6. Official Weather and Emergency Information")

st.markdown(
    """
    - **India Meteorological Department (IMD):**
      https://mausam.imd.gov.in/

    - **National Disaster Management Authority (NDMA):**
      https://ndma.gov.in/

    - **National Disaster Response Force (NDRF):**
      https://ndrf.gov.in/
    """
)

st.caption(
    "CycloneAI is an educational prototype. Its illustrative "
    "categories do not represent official warnings or validated "
    "predictions of real-world impacts."
)