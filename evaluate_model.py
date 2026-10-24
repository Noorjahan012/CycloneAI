import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error

print("Loading dataset...")

file_path = "data/ibtracs.since1980.list.v04r01.csv"

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

print("Dataset loaded.")

# Prepare data in the same way as the training script
for col in ["LAT", "LON", "USA_WIND", "WMO_WIND"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["WIND"] = df["USA_WIND"].fillna(df["WMO_WIND"])

df["ISO_TIME"] = pd.to_datetime(
    df["ISO_TIME"],
    errors="coerce"
)

df = df.dropna(
    subset=["SID", "ISO_TIME", "LAT", "LON", "WIND"]
)

df = df[
    (df["WIND"] >= 0)
    & df["LAT"].between(-90, 90)
    & df["LON"].between(-180, 180)
].copy()

df = df.sort_values(["SID", "ISO_TIME"]).copy()
df["MONTH"] = df["ISO_TIME"].dt.month

df["NEXT_WIND"] = df.groupby("SID")["WIND"].shift(-1)
df = df.dropna(subset=["NEXT_WIND"]).copy()

features = ["LAT", "LON", "WIND", "MONTH"]
target = "NEXT_WIND"

df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna(subset=features + [target])

print("Prepared observations:", len(df))
print("Number of cyclones:", df["SID"].nunique())

if df["SID"].nunique() < 2:
    raise ValueError("At least two different cyclones are required.")

# Recreate the same group-based test split
splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=42
)

train_idx, test_idx = next(
    splitter.split(df[features], df[target], groups=df["SID"])
)

X_test = df.iloc[test_idx][features]
y_test = df.iloc[test_idx][target]

print("Loading saved model...")

saved = joblib.load("models/intensity_model.pkl")
model = saved["model"]

print("Generating predictions...")

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

print("\n===== CYCLONE INTENSITY MODEL EVALUATION =====")
print(f"Test observations: {len(y_test)}")
print(f"Test cyclones: {df.iloc[test_idx]['SID'].nunique()}")
print(f"MAE: {mae:.2f} knots")
print(f"RMSE: {rmse:.2f} knots")

print("\n===== SAMPLE PREDICTIONS =====")

results = pd.DataFrame({
    "Actual wind speed (knots)": y_test.values[:10],
    "Predicted wind speed (knots)": predictions[:10]
})

print(results.round(2).to_string(index=False))

print("\nEvaluation completed.")
