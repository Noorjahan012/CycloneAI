import pandas as pd
from pathlib import Path

# Original historical cyclone dataset
source = Path("data/ibtracs.since1980.list.v04r01.csv")

# New, smaller dataset for deployment
destination = Path("data/ibtracs_compact.csv")

# Check whether the original dataset exists
if not source.exists():
    print("ERROR: Original cyclone dataset was not found.")
    print("Expected location:", source.resolve())
    raise SystemExit(1)

print("Reading the original cyclone dataset...")

# Keep only the columns required for cyclone tracking
columns = [
    "SID",
    "NAME",
    "ISO_TIME",
    "LAT",
    "LON",
    "USA_WIND",
    "WMO_WIND"
]

df = pd.read_csv(
    source,
    skiprows=[1],
    usecols=columns,
    low_memory=False
)

# Save the smaller dataset without modifying the original
df.to_csv(destination, index=False)

# Display the results
size_mb = destination.stat().st_size / (1024 * 1024)

print("\nDataset preparation completed!")
print("Number of records:", len(df))
print("Columns retained:", ", ".join(columns))
print(f"New dataset size: {size_mb:.2f} MB")
print("Saved to:", destination.resolve())