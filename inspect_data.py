
import pandas as pd
from pathlib import Path

file_path = Path("data/ibtracs.since1980.list.v04r01.csv")

if not file_path.exists():
    print("CSV file not found!")
    print("Check the filename and the data folder.")
else:
    df = pd.read_csv(
        file_path,
        low_memory=False,
        nrows=10
    )

    print("Dataset loaded successfully!")
    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head().to_string())

    print("\nDataset shape for inspected rows:")
    print(df.shape)
