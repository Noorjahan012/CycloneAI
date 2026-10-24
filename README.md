# CycloneAI — AI-Based Cyclone Prediction and Decision Support

CycloneAI is a prototype application designed to explore how artificial intelligence and historical cyclone data can support cyclone intensity estimation, track visualization, impact awareness, and evacuation preparedness.

## Features

- **Main Dashboard:** Estimates cyclone wind intensity using a trained machine learning model.
- **Historical Cyclone Track Map:** Visualizes historical cyclone movement.
- **Cyclone Track Forecast:** Estimates future cyclone positions using recent recorded movement.
- **Impact Assessment:** Displays illustrative impact categories based on wind speed.
- **Evacuation Support:** Provides preparedness guidance and links to official disaster-management resources.

## Technologies Used

- Python
- Streamlit
- Pandas and NumPy
- Scikit-learn
- Joblib
- Folium
- Streamlit-Folium
- NOAA IBTrACS historical cyclone dataset

## Project Structure

```text
CycloneAI/
├── data/
├── models/
├── pages/
├── app.py
├── evaluate_model.py
├── inspect_data.py
├── track_map.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Usage

1. Install Python on your computer.
2. Clone or download the project.
3. Open a terminal in the project directory.
4. Create and activate a Python virtual environment.
5. Install the dependencies:

   `pip install -r requirements.txt`

6. Start the application:

   `streamlit run app.py`

7. Open the local address displayed in the terminal.

## Dataset

The project uses historical cyclone observations from the NOAA International Best Track Archive for Climate Stewardship (IBTrACS).

The dataset must be available in the location and format expected by the application.

## Limitations and Safety

CycloneAI is an experimental educational prototype, not an operational meteorological forecasting or emergency-warning system.

- Intensity estimates depend on the model and input data.
- Track forecasts use simplified movement extrapolation and may be inaccurate.
- Impact categories are illustrative and do not represent a validated local damage model.
- The application does not issue official warnings or evacuation orders.

For real-time cyclone warnings and evacuation instructions, consult the India Meteorological Department and relevant government disaster-management authorities.