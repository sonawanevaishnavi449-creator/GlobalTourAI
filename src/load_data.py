import pandas as pd

file_path = "D:\GlobalTourAI\Datasets\Raw_Dataset\india_tourism_dataset.json"

tourism_df = pd.read_json(file_path)

print(tourism_df.head())

print("\nShape:")
print(tourism_df.shape)

print("\nColumns:")
print(tourism_df.columns)

print("\nInformation")
print(tourism_df.info)