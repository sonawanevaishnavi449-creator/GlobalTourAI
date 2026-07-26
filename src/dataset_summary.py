import pandas as pd

Tourism_data = pd.read_csv("D:\GlobalTourAI\Datasets\Tourist_places.csv")

print("=" * 50)
print("GLOBALTOURAI DATASET SUMMARY")
print("=" * 50)

print("\nDataset Shape")
print(Tourism_data.shape)

print("\nColumn Names")
print(Tourism_data.columns)

print("\nData Types")
print(Tourism_data.dtypes)

print("\nDataset Information")
print(Tourism_data.info())

print("\nStatistical Summary")
print(Tourism_data.describe(include="all"))