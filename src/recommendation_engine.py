import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

#Creating one column for combining all descripion

clean_df["search_text"] = (
    clean_df["trip_types"].astype(str)
    + " "
    + clean_df["activities_available"].astype(str)
    + " "
    + clean_df["primary_attractions"].astype(str)
    + " "
    + clean_df["unique_experiences"].astype(str)
)

print(
    clean_df[
        ["destination_name","search_text"]
    ].head()
)

print(
    clean_df[
        ["destination_name","search_text"]
    ].tail()
)

vectorizer= TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(clean_df["search_text"])
print(tfidf_matrix.shape)





print("*"*100)
print("\nWELCOME IN GLOBAL TOUR AI SYSTEM")
print("*"*100)

print("\nHello")

print("\nWhat you want to explore in this world ? ")
query=input("Enter Your Query:  ")

#query =  "mountains trekking adventure"
query_vector = vectorizer.transform([query])
similarity_scores = cosine_similarity(query_vector, tfidf_matrix)
best_match = similarity_scores.argmax()

similarity_scores = similarity_scores.flatten()

top_5 = similarity_scores.argsort()[-5:][::-1]

print("=" * 60)
print("TOP 5 RECOMMENDATIONS")
print("=" * 60)

for i in top_5:
    print(f"\nDestination : {clean_df.iloc[i]['destination_name']}")
    print(f"State       : {clean_df.iloc[i]['state']}")
    print(f"Score       : {similarity_scores[i]:.3f}")


