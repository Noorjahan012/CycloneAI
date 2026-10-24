
import pandas as pd
import numpy as np
import os
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error

print("Loading cyclone dataset...")

file_path = "data/ibtracs.since1980.list.v04r01.csv"

# Read only the columns needed for our first model
df = pd.read_csv(
    file_path,
    skiprows=[1],
    usecols=[
        "SID",
        "ISO_TIME",
        "LAT",
        "LON",
        "USA_WIND",
        "WMO_WIND"
    ],
    low_memory=False
)

print("Dataset loaded!")
print("Preparing data...")

# Convert columns to numeric values
for col in ["LAT", "LON", "USA_WIND", "WMO_WIND"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Use USA wind speed when available, otherwise use WMO wind speed
df["WIND"] = df["USA_WIND"].fillna(df["WMO_WIND"])

# Convert observation time to datetime
df["ISO_TIME"] = pd.to_datetime(
    df["ISO_TIME"],
    errors="coerce"
)

# Remove records with missing essential information
df = df.dropna(
    subset=["SID", "ISO_TIME", "LAT", "LON", "WIND"]
)

# Remove invalid wind speeds and impossible coordinates
df = df[
    (df["WIND"] >= 0) &
    (df["LAT"].between(-90, 90)) &
    (df["LON"].between(-180, 180))
].copy()

# Sort observations by cyclone and time
df = df.sort_values(["SID", "ISO_TIME"]).copy()

# Extract month from the observation date
df["MONTH"] = df["ISO_TIME"].dt.month

# Target: wind speed at the next observation of the same cyclone
df["NEXT_WIND"] = df.groupby("SID")["WIND"].shift(-1)

# Keep rows that have a next observation
df = df.dropna(subset=["NEXT_WIND"]).copy()

features = ["LAT", "LON", "WIND", "MONTH"]
target = "NEXT_WIND"

# Remove records with invalid feature or target values
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna(subset=features + [target])

print("Prepared observations:", len(df))
print("Number of cyclones:", df["SID"].nunique())

if df["SID"].nunique() < 2:
    raise ValueError(
        "Not enough different cyclones to create a training and test split."
    )

# Split by cyclone so observations from the same cyclone
# do not appear in both training and testing sets
splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=42
)

train_idx, test_idx = next(
    splitter.split(df[features], df[target], groups=df["SID"])
)

X_train = df.iloc[train_idx][features]
X_test = df.iloc[test_idx][features]

y_train = df.iloc[train_idx][target]
y_test = df.iloc[test_idx][target]

print("Training the model...")

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Evaluating the model...")

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

print("\nMODEL EVALUATION")
print("-------------------------")
print(f"Mean Absolute Error: {mae:.2f} knots")
print(f"Root Mean Squared Error: {rmse:.2f} knots")

# Save the trained model
os.makedirs("models", exist_ok=True)

joblib.dump(
    {
        "model": model,
        "features": features,
        "target": target,
        "wind_unit": "knots"
    },
    "models/intensity_model.pkl"
)

print("\nModel saved successfully!")
print("Location: models/intensity_model.pkl")
print("\nTraining completed!")
