import pandas as pd

Data = {

    "Place":
    [
    "Tajmahal",
    "Eiffel Tower",
    "Goa Beach",
    "Mount Fuji",
    "Pandharpur",
    "Bramhagiri"
    ],


    "City":
    [
        "Agra",
        "Paris",
        "Goa",
        "Tokyo",
        "Pune",
        "Nashik"
    ],

    "Country":
    [
    "India",
    "France",
    "India",
    "Japan",
    "India",
    "India"
    ],

    "Category":
    [
    "Monument",
    "Monument",
    "Beach",
    "Mountain",
    "Temple",
    "Mountain"
    ]

    

}

Tourism_DF=pd.DataFrame(Data)

print(Tourism_DF)

Tourism_DF.head()
Tourism_DF.tail()
Tourism_DF.describe()
Tourism_DF.info()

print("\nFirst 3 rows:")
print(Tourism_DF.head(3))

print("\nLast 2 rows:")
print(Tourism_DF.tail(2))

print("\nColumn Names:")
print(Tourism_DF.columns)

print("\nDataset Shape:")
print(Tourism_DF.shape)