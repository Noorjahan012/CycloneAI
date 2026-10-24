import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from pathlib import Path

st.set_page_config(page_title="CycloneAI Track Map", layout="wide")

st.title("🌪️ Historical Cyclone Track Map")
st.write("Explore historical cyclone paths from the NOAA IBTrACS dataset.")

DATA_FILE = Path("data/ibtracs_compact.csv")

if not DATA_FILE.exists():
    st.error(f"Dataset not found: {DATA_FILE}")
    st.stop()


@st.cache_data(show_spinner="Loading historical cyclone data...")
def load_data(file_path):
    required_columns = [
        "SID", "NAME", "ISO_TIME", "LAT", "LON", "USA_WIND", "WMO_WIND"
    ]

    # Read only the columns needed for the map.
    # IBTrACS contains a units row after its column-header row.
    df = pd.read_csv(
        file_path,
        skiprows=[1],
        usecols=lambda col: col in required_columns,
        low_memory=False
    )

    for col in ["LAT", "LON", "USA_WIND", "WMO_WIND"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["SID", "LAT", "LON"])

    df = df[
        df["LAT"].between(-90, 90)
        & df["LON"].between(-180, 180)
    ].copy()

    df["ISO_TIME"] = pd.to_datetime(df["ISO_TIME"], errors="coerce")

    return df


try:
    df = load_data(str(DATA_FILE))

    if df.empty:
        st.warning("No valid cyclone track records were found.")
        st.stop()

    # Build a cyclone selector.
    cyclone_options = (
        df.groupby("SID", sort=False)["NAME"]
        .first()
        .fillna("Unnamed cyclone")
    )

    selected_sid = st.selectbox(
        "Select a historical cyclone",
        cyclone_options.index.tolist(),
        format_func=lambda sid: (
            f"{cyclone_options.loc[sid]} — {sid}"
        )
    )

    track = df[df["SID"] == selected_sid].copy()
    track = track.sort_values("ISO_TIME")

    if track.empty:
        st.warning("No positions are available for this cyclone.")
        st.stop()

    first = track.iloc[0]

    cyclone_map = folium.Map(
        location=[first["LAT"], first["LON"]],
        zoom_start=4
    )

    points = track[["LAT", "LON"]].values.tolist()

    if len(points) > 1:
        folium.PolyLine(
            points,
            color="red",
            weight=3,
            tooltip="Recorded historical cyclone path"
        ).add_to(cyclone_map)

    for _, row in track.iterrows():
        details = [
            f"Latitude: {row['LAT']}",
            f"Longitude: {row['LON']}"
        ]

        if pd.notna(row["ISO_TIME"]):
            details.append(f"Time: {row['ISO_TIME']}")

        wind = None

        for column in ["USA_WIND", "WMO_WIND"]:
            if column in track.columns and pd.notna(row[column]):
                wind = row[column]
                break

        if wind is not None:
            details.append(f"Wind speed: {wind} knots")

        folium.CircleMarker(
            location=[row["LAT"], row["LON"]],
            radius=4,
            popup="<br>".join(details),
            color="blue",
            fill=True
        ).add_to(cyclone_map)

    st_folium(cyclone_map, width=None, height=550, key="cyclone_map")

    st.success(f"Loaded {len(track)} historical positions.")

    st.caption(
        "This map shows historical observations only. "
        "It does not predict a cyclone's future track."
    )

except Exception as error:
    st.error("Unable to display the historical cyclone map.")
    st.exception(error)
