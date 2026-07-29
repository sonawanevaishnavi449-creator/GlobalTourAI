import pandas as pd

clean_df=pd.read_csv("D:\GlobalTourAI\Datasets\Processed_Data.csv") 

print("*" * 100)
print("\ndata loaded successfully")
print("=" * 100)
print(clean_df.head(5))
print("=" * 100)

features = [
    "destination_name",
    "state",
    "trip_types",
    "primary_attractions",
    "activities_available",
    "unique_experiences",
    "budget_daily_min",
    "budget_daily_max",
    "ideal_days",
    "Winter_Temp",
    "Summer_Temp",
    "Monsoon_Temp"
]

recommendation_df = clean_df[features]

print(recommendation_df.head())
