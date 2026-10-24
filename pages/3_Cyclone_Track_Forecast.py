import streamlit as st
import pandas as pd
import folium
from pathlib import Path
from streamlit_folium import st_folium


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Cyclone Track Forecast | CycloneAI",
    page_icon="🌪️",
    layout="wide"
)

st.title("🌪️ CycloneAI - Track Forecasting")
st.write(
    "Explore historical cyclone tracks and estimate future positions "
    "using a simple movement-based forecasting method."
)

st.warning(
    "Experimental demonstration only. These estimates are not official "
    "forecasts and must not be used for evacuation or safety decisions."
)


# --------------------------------------------------
# LOAD HISTORICAL DATA
# --------------------------------------------------

DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "ibtracs_compact.csv"
    )


@st.cache_data(show_spinner="Loading historical cyclone data...")
def load_data(file_path):

    columns = [
        "SID",
        "NAME",
        "ISO_TIME",
        "LAT",
        "LON",
        "USA_WIND",
        "WMO_WIND"
    ]

    data = pd.read_csv(
        file_path,
        usecols=columns,
        skiprows=[1],
        low_memory=False
    )

    data["ISO_TIME"] = pd.to_datetime(
        data["ISO_TIME"],
        errors="coerce",
        utc=True
    )

    for column in ["LAT", "LON", "USA_WIND", "WMO_WIND"]:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    # Prefer USA_WIND when available; otherwise use WMO_WIND.
    data["WIND"] = data["USA_WIND"].fillna(data["WMO_WIND"])

    data = data.dropna(
        subset=["SID", "ISO_TIME", "LAT", "LON"]
    )

    # Remove invalid geographic coordinates.
    data = data[
        data["LAT"].between(-90, 90)
        & data["LON"].between(-180, 180)
    ]

    data = data.sort_values(["SID", "ISO_TIME"])

    return data


if not DATA_PATH.exists():
    st.error(f"Dataset not found: {DATA_PATH}")
    st.info(
        "Check that the original IBTrACS CSV file exists "
        "inside the project's data folder."
    )
    st.stop()


try:
    data = load_data(str(DATA_PATH))
except Exception as error:
    st.error("Unable to load the cyclone dataset.")
    st.exception(error)
    st.stop()


if data.empty:
    st.error("No valid cyclone observations were found.")
    st.stop()


# --------------------------------------------------
# SELECT A CYCLONE
# --------------------------------------------------

st.subheader("1. Select a Historical Cyclone")

cyclones = (
    data[["SID", "NAME"]]
    .drop_duplicates()
    .sort_values(["NAME", "SID"])
    .reset_index(drop=True)
)

cyclones["NAME"] = cyclones["NAME"].fillna("UNNAMED")

cyclones["LABEL"] = (
    cyclones["NAME"].astype(str)
    + " | "
    + cyclones["SID"].astype(str)
)

selected_label = st.selectbox(
    "Choose a cyclone",
    cyclones["LABEL"].tolist()
)

selected_sid = cyclones.loc[
    cyclones["LABEL"] == selected_label,
    "SID"
].iloc[0]


storm = data[data["SID"] == selected_sid].copy()
storm = storm.sort_values("ISO_TIME").reset_index(drop=True)

if len(storm) < 2:
    st.error(
        "This cyclone has fewer than two valid observations. "
        "Track estimation requires at least two positions."
    )
    st.stop()


# --------------------------------------------------
# DISPLAY HISTORICAL INFORMATION
# --------------------------------------------------

latest = storm.iloc[-1]

col1, col2, col3 = st.columns(3)

col1.metric("Recorded observations", len(storm))

col2.metric(
    "Latest recorded wind",
    (
        f"{latest['WIND']:.1f} knots"
        if pd.notna(latest["WIND"])
        else "Unavailable"
    )
)

col3.metric(
    "Latest record date",
    latest["ISO_TIME"].strftime("%Y-%m-%d %H:%M UTC")
)

st.caption(
    "The latest observation is the latest record available for the "
    "selected cyclone in the downloaded dataset. It may be historical, "
    "not the cyclone's current position."
)


# --------------------------------------------------
# FORECAST SETTINGS
# --------------------------------------------------

st.subheader("2. Estimate a Future Position")

forecast_hours = st.selectbox(
    "Estimate position after",
    [6, 12, 24, 48],
    index=1,
    format_func=lambda hours: f"{hours} hours"
)


# --------------------------------------------------
# ESTIMATE MOVEMENT FROM THE LAST TWO POSITIONS
# --------------------------------------------------

# Select the last two observations with different timestamps.
unique_times = storm.drop_duplicates(
    subset=["ISO_TIME"],
    keep="last"
)

if len(unique_times) < 2:
    st.error(
        "Two observations with different timestamps are required."
    )
    st.stop()

previous = unique_times.iloc[-2]
latest = unique_times.iloc[-1]

elapsed_hours = (
    latest["ISO_TIME"] - previous["ISO_TIME"]
).total_seconds() / 3600

if elapsed_hours <= 0:
    st.error(
        "The last two observations do not have a valid time interval."
    )
    st.stop()


# Calculate latitude movement per hour.
latitude_change = latest["LAT"] - previous["LAT"]

latitude_rate = latitude_change / elapsed_hours


# Calculate longitude movement per hour.
# This adjustment avoids an incorrect large jump across the
# International Date Line.
longitude_change = latest["LON"] - previous["LON"]

longitude_change = (
    (longitude_change + 180) % 360
) - 180

longitude_rate = longitude_change / elapsed_hours


# Extrapolate position using constant movement.
predicted_lat = (
    latest["LAT"] + latitude_rate * forecast_hours
)

predicted_lon = (
    latest["LON"] + longitude_rate * forecast_hours
)

# Keep coordinates within valid geographic ranges.
predicted_lat = max(-90, min(90, predicted_lat))

# Normalize longitude to the range -180 to 180.
predicted_lon = (
    (predicted_lon + 180) % 360
) - 180

predicted_time = (
    latest["ISO_TIME"]
    + pd.Timedelta(hours=forecast_hours)
)


# --------------------------------------------------
# DISPLAY ESTIMATED POSITION
# --------------------------------------------------

st.subheader("3. Estimated Position")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Estimated latitude",
    f"{predicted_lat:.3f}°"
)

col2.metric(
    "Estimated longitude",
    f"{predicted_lon:.3f}°"
)

col3.metric(
    "Estimated time",
    predicted_time.strftime("%Y-%m-%d %H:%M UTC")
)

st.write(
    "The estimate assumes that the cyclone continues moving at "
    "approximately the same coordinate-based rate as between its "
    "last two recorded observations."
)


# --------------------------------------------------
# CREATE THE MAP
# --------------------------------------------------

st.subheader("4. Historical Track and Estimated Position")

historical_points = [
    [row["LAT"], row["LON"]]
    for _, row in storm.iterrows()
]

forecast_point = [predicted_lat, predicted_lon]

cyclone_map = folium.Map(
    location=[latest["LAT"], latest["LON"]],
    zoom_start=4,
    tiles="OpenStreetMap"
)


# Draw the historical path.
folium.PolyLine(
    historical_points,
    color="blue",
    weight=3,
    opacity=0.8,
    tooltip="Historical recorded track"
).add_to(cyclone_map)


# Mark the latest recorded position.
folium.Marker(
    location=[latest["LAT"], latest["LON"]],
    popup=(
        f"Latest recorded position<br>"
        f"Latitude: {latest['LAT']:.3f}<br>"
        f"Longitude: {latest['LON']:.3f}<br>"
        f"Time: {latest['ISO_TIME']}"
    ),
    tooltip="Latest recorded position",
    icon=folium.Icon(color="blue", icon="info-sign")
).add_to(cyclone_map)


# Draw the estimated movement line.
folium.PolyLine(
    [
        [latest["LAT"], latest["LON"]],
        forecast_point
    ],
    color="red",
    weight=3,
    dash_array="8, 8",
    tooltip="Experimental estimated movement"
).add_to(cyclone_map)


# Mark the estimated position.
folium.Marker(
    location=forecast_point,
    popup=(
        f"Experimental estimated position<br>"
        f"Latitude: {predicted_lat:.3f}<br>"
        f"Longitude: {predicted_lon:.3f}<br>"
        f"Estimated time: {predicted_time}"
    ),
    tooltip="Experimental estimated position",
    icon=folium.Icon(color="red", icon="flag")
).add_to(cyclone_map)


# Zoom to include the historical and estimated positions.
all_points = historical_points + [forecast_point]

cyclone_map.fit_bounds(all_points)

st_folium(
    cyclone_map,
    width=None,
    height=550,
    key="cyclone_track_forecast_map"
)


# --------------------------------------------------
# LIMITATIONS
# --------------------------------------------------

with st.expander("Understand the limitations"):

    st.write(
        """
        - This is a constant-movement extrapolation baseline, not a
          trained AI track-prediction model.
        - Real cyclone movement can change because of atmospheric
          circulation, environmental conditions, and other factors.
        - The time interval between recorded observations can vary.
        - The estimate does not calculate a prediction cone or
          quantify uncertainty.
        - This page does not predict landfall or determine evacuation
          requirements.
        - Historical observations and this experimental estimate
          must not replace official meteorological forecasts.
        """
    )

st.info(
    "For real-world cyclone warnings and evacuation decisions, "
    "follow official meteorological and disaster-management authorities."
)