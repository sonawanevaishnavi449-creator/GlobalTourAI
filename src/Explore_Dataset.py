import pandas as pd

file_path = "D:\GlobalTourAI\Datasets\Raw_Dataset\india_tourism_dataset.json"

tourism_df = pd.read_json(file_path)

print("="*100)
print("\nReal Tourism Data Anlysis")
print("="*100)

print(tourism_df.head())

print("\nShape:")
print(tourism_df.shape)

print("\nColumns:")
print(tourism_df.columns)

print("\nInformation")
print(tourism_df.info)

print("\nStatistical summary")
print(tourism_df.describe())

print("\nFirst 5 Destinations:")
print(tourism_df.head())

print(tourism_df.isnull().sum())

print(tourism_df.dtypes)

duplicates = tourism_df["destination_name"].duplicated().sum()

print("Duplicate destination names:", duplicates)

duplicates = tourism_df[
    tourism_df["destination_name"].duplicated(keep=False)
]

print(duplicates[["destination_name", "state", "district"]].sort_values("destination_name"))

print("Duplicate Rows")

duplicate_rows = tourism_df[
    tourism_df.duplicated(subset=["destination_name", "state", "district"], keep=False)
]

print(duplicate_rows)

print("=" * 80)

print(tourism_df.loc[13])
print("=" * 80)
print(tourism_df.loc[72])

print("=" * 80)
print(tourism_df.loc[7])
print("=" * 80)
print(tourism_df.loc[52])
