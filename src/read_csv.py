import pandas as pd

df=pd.read_csv("D:\GlobalTourAI\Datasets\Tourist_places.csv")

print(df.head())
print(df.head(3))
print(df.tail())
print(df.shape)
print(df.columns)
print(df.info())
print(df.describe())