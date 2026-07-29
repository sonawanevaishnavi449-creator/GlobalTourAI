import pandas as pd

tourism_df = pd.read_json("D:\GlobalTourAI\Datasets\Raw_Dataset\india_tourism_dataset.json")

print("Dataset Loaded Successfully!")

print("=" * 90)

print(tourism_df.head(5))

print("=" * 90)

print(tourism_df["coordinates"].iloc[0])
tourism_df["latitude"] = tourism_df["coordinates"].apply(lambda x: x["latitude"])
tourism_df["longitude"] = tourism_df["coordinates"].apply(lambda x: x["longitude"])

print(tourism_df[["destination_name", "latitude", "longitude"]].head(10))

tourism_df["airport_name"] = tourism_df["nearest_airport"].apply(lambda x: x["name"])

tourism_df["airport_distance_km"] = tourism_df["nearest_airport"].apply(lambda x: x["distance_km"])

print(
    tourism_df[
        [
            "destination_name",
            "airport_name",
            "airport_distance_km"
        ]
    ].head()
)

tourism_df["railway_station_name"] = tourism_df["nearest_railway_station"].apply(lambda x: x["name"])
tourism_df["railway_distance_km"] = tourism_df["nearest_railway_station"].apply(lambda x: x["distance_km"])  

print(
  tourism_df[
      [
          "destination_name",
          "railway_station_name",
          "railway_distance_km"

      ]
  ].head() 
)

tourism_df["major_city_name"]=tourism_df["nearest_major_city"].apply(lambda x: x["name"])
tourism_df["major_city_km"]=tourism_df["nearest_major_city"].apply(lambda x: x["distance_km"])

print(
    tourism_df[
        [
            "destination_name",
            "major_city_name",
            "major_city_km"
        ]
    ].head()
)


tourism_df["Winter_Temp"]=tourism_df["average_temperature"].apply(lambda x: x["winter"])
tourism_df["Summer_Temp"]=tourism_df["average_temperature"].apply(lambda x: x["summer"])
tourism_df["Monsoon_Temp"]=tourism_df["average_temperature"].apply(lambda x: x["monsoon"])

print(
    tourism_df[
        [
            "destination_name",
            "Winter_Temp",
            "Summer_Temp",
            "Monsoon_Temp"

        ]
    ].head()
)



tourism_df["budget_accommodation_min"] = tourism_df["budget_category"].apply(lambda x: x["accommodation_range"][0])

tourism_df["budget_accommodation_max"] = tourism_df["budget_category"].apply(lambda x: x["accommodation_range"][1])

tourism_df["budget_food_min"] = tourism_df["budget_category"].apply(lambda x: x["food_range"][0])

tourism_df["budget_food_max"] = tourism_df["budget_category"].apply(lambda x: x["food_range"][1])

tourism_df["budget_activity_min"] = tourism_df["budget_category"].apply(lambda x: x["activities_range"][0])

tourism_df["budget_activity_max"] = tourism_df["budget_category"].apply(lambda x: x["activities_range"][1])

tourism_df["budget_transport_min"] = tourism_df["budget_category"].apply(lambda x: x["local_transport_range"][0])

tourism_df["budget_transport_max"] = tourism_df["budget_category"].apply(lambda x: x["local_transport_range"][1])

tourism_df["budget_daily_min"] = tourism_df["budget_category"].apply(lambda x: x["total_daily_range"][0])

tourism_df["budget_daily_max"] = tourism_df["budget_category"].apply(lambda x: x["total_daily_range"][1])

print(
    tourism_df[
        [
            "destination_name",
            "budget_daily_min",
            "budget_daily_max"
        ]
    ].head()
)

print("for mid range")

tourism_df["min_accommodation_range"]=tourism_df["mid_range_category"].apply(lambda x: x["accommodation_range"][0])
tourism_df["max_accommodation_range"]=tourism_df["mid_range_category"].apply(lambda x: x["accommodation_range"][1])

tourism_df["min_food_range"]=tourism_df["mid_range_category"].apply(lambda x: x["food_range"][0])
tourism_df["max_food_range"]=tourism_df["mid_range_category"].apply(lambda x: x["food_range"][1])

tourism_df["min_activity_range"]=tourism_df["mid_range_category"].apply(lambda x: x["activities_range"][0])
tourism_df["max_activity_range"]=tourism_df["mid_range_category"].apply(lambda x: x["activities_range"][1])

tourism_df["min_local_transport_range"]=tourism_df["mid_range_category"].apply(lambda x: x["local_transport_range"][0])
tourism_df["max_local_transport_range"]=tourism_df["mid_range_category"].apply(lambda x: x["local_transport_range"][1])

tourism_df["min_total_daily_range"]=tourism_df["mid_range_category"].apply(lambda x: x["total_daily_range"][0])
tourism_df["max_total_daily_range"]=tourism_df["mid_range_category"].apply(lambda x: x["total_daily_range"][1])

print(
    tourism_df[
        [
            "destination_name",
            "min_total_daily_range",
            "max_total_daily_range"
            


        ]
    ].head()
)

print("For Luxurious")

tourism_df["min_accommodation_range"]=tourism_df["luxury_category"].apply(lambda x: x["accommodation_range"][0])
tourism_df["max_accommodation_range"]=tourism_df["luxury_category"].apply(lambda x: x["accommodation_range"][1])

tourism_df["min_food_range"]=tourism_df["luxury_category"].apply(lambda x: x["food_range"][0])
tourism_df["max_food_range"]=tourism_df["luxury_category"].apply(lambda x: x["food_range"][1])

tourism_df["min_activity_range"]=tourism_df["luxury_category"].apply(lambda x: x["activities_range"][0])
tourism_df["max_activity_range"]=tourism_df["luxury_category"].apply(lambda x: x["activities_range"][1])

tourism_df["min_local_transport_range"]=tourism_df["luxury_category"].apply(lambda x: x["local_transport_range"][0])
tourism_df["max_local_transport_range"]=tourism_df["luxury_category"].apply(lambda x: x["local_transport_range"][1])

tourism_df["min_total_daily_range"]=tourism_df["luxury_category"].apply(lambda x: x["total_daily_range"][0])
tourism_df["max_total_daily_range"]=tourism_df["luxury_category"].apply(lambda x: x["total_daily_range"][1])



print(
    tourism_df[
        [
            "destination_name",
            "min_total_daily_range",
            "max_total_daily_range"
            


        ]
    ].head()
)

print(tourism_df.columns)


tourism_df = tourism_df.drop(columns=[
    "coordinates",
    "nearest_airport",
    "nearest_railway_station",
    "nearest_major_city",
    "average_temperature",
    "budget_category",
    "mid_range_category",
    "luxury_category"
])

print(tourism_df.shape)
print(tourism_df.info())

tourism_df.to_csv(
    "D:\GlobalTourAI\Datasets\Processed_Data.csv",
    index=False
)

tourism_df.to_json(
    "D:\GlobalTourAI\Datasets\Processed_Data.json",
    orient="records",
    indent=4
)


clean_df=pd.read_csv("D:\GlobalTourAI\Datasets\Processed_Data.csv") 
print(clean_df.head(5)) 
print(clean_df.shape)                                                          