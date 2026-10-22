import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer

# =========================================================
# 1. INITIALIZATION AND DATASET LOADING
# =========================================================

DATASET_PATH = r"D:\GlobalTourAI\Datasets\Processed_Data.csv"

stemmer = PorterStemmer()
clean_df = pd.read_csv(DATASET_PATH)

# =========================================================
# 2. TEXT PREPROCESSING AND QUERY EXPANSION
# =========================================================

def preprocess_text(text):
    """Convert text to lowercase and stem its words."""
    words = str(text).lower().split()
    return " ".join(stemmer.stem(word) for word in words)


QUERY_SYNONYMS = {
    "beach": (
        "beach beaches coastal coast seaside shoreline shore sea ocean "
        "island swimming water sports sunset"
    ),
    "mountain": (
        "mountain mountains hill hills trekking hiking peaks valley nature"
    ),
    "temple": (
        "temple temples shrine pilgrimage spiritual religious worship "
        "prayer darshan architecture heritage"
    ),
    "fort": (
        "fort forts fortress castle citadel palace ramparts historic "
        "historical heritage architecture kingdom"
    ),
    "traditional": (
        "traditional culture heritage historic historical architecture "
        "monument monuments fort forts temple temples palace palaces"
    ),
    "history": (
        "history historical heritage monument monuments fort forts palace "
        "palaces archaeology culture ancient kingdom"
    ),
    "heritage": (
        "heritage historic historical architecture fort forts temple temples "
        "palace palaces monument monuments culture"
    ),
    "wildlife": (
        "wildlife animals safari forest birds national park nature sanctuary"
    ),
    "food": (
        "food cuisine local dishes street food restaurants culinary"
    ),
}


def expand_query(query):
    """Expand common travel interests with related search terms."""
    query_lower = str(query).lower()
    extra_terms = []
    for keyword, related_terms in QUERY_SYNONYMS.items():
        if keyword in query_lower:
            extra_terms.append(related_terms)
    return preprocess_text(" ".join([str(query)] + extra_terms))


# =========================================================
# 3. RECOMMENDATION ENGINE
# =========================================================

def recommend_destinations(query, budget, days, season, traveler):
    df = clean_df.copy()

    required_columns = [
        "best_seasons", "ideal_for", "budget_daily_min", "budget_daily_max",
        "minimum_days", "destination_name", "state", "ideal_days",
        "popularity_score", "safety_rating"
    ]
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        print("Dataset is missing required columns:", ", ".join(missing_columns))
        return []

    # Convert numeric fields safely.
    numeric_columns = [
        "budget_daily_min", "budget_daily_max", "minimum_days",
        "ideal_days", "popularity_score", "safety_rating"
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Keep the daily budget limit strict.
    candidates = df[
        df["budget_daily_max"].notna()
        & (df["budget_daily_max"] <= budget)
    ].copy()
    print("\nDestinations within daily budget:", len(candidates))

    if candidates.empty:
        print(f"No destinations have a recorded maximum daily budget within ₹{budget:,.0f}.")
        print("Try increasing your daily budget.")
        return []

    # Duration is a preference, not a hard stop: allow a shorter suggested trip
    # to appear, but favor places whose minimum duration fits the user's trip.
    duration_fit = (
        candidates["minimum_days"].notna()
        & (candidates["minimum_days"] <= days)
    )
    print("Destinations whose minimum duration fits:", int(duration_fit.sum()))

    # Make search text from useful available dataset columns.
    text_columns = [
        "destination_name", "state", "best_seasons", "ideal_for", "trip_types",
        "activities_available", "primary_attractions", "unique_experiences",
        "local_culture", "hidden_gems", "local_cuisine_must_try",
        "festivals_events", "local_customs", "sustainability_notes",
        "description", "destination_type", "category", "historical_significance"
    ]
    available_columns = [column for column in text_columns if column in candidates.columns]
    if not available_columns:
        print("No searchable text columns were found in the dataset.")
        return []

    candidates["search_text"] = (
        candidates[available_columns]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
        .apply(preprocess_text)
    )
    candidates = candidates[candidates["search_text"].str.strip().ne("")].copy()
    if candidates.empty:
        print("The candidate destinations do not contain searchable text.")
        return []

    # TF-IDF similarity for the user's interest.
    processed_query = expand_query(query)
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        tfidf_matrix = vectorizer.fit_transform(candidates["search_text"])
        query_vector = vectorizer.transform([processed_query])
    except ValueError:
        print("Unable to create searchable text from the dataset.")
        return []

    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
    print("TF-IDF matrix shape:", tfidf_matrix.shape)
    print("Similarity scores calculated successfully.")

    # Preference matches are soft scoring bonuses rather than hard filters.
    season_match = candidates["best_seasons"].astype(str).str.contains(
        str(season), case=False, na=False
    ).to_numpy(dtype=float)
    traveler_match = candidates["ideal_for"].astype(str).str.replace(
        "_", " ", regex=False
    ).str.contains(
        str(traveler).replace("_", " "), case=False, na=False
    ).to_numpy(dtype=float)

    popularity = candidates["popularity_score"].fillna(0).clip(0, 10).to_numpy() / 10
    safety = candidates["safety_rating"].fillna(0).clip(0, 10).to_numpy() / 10

    # Prioritize interest relevance; use season, traveler, duration,
    # popularity and safety as smaller secondary signals.
    final_scores = (
        0.80 * similarity_scores
        + 0.05 * season_match
        + 0.05 * traveler_match
        + 0.04 * duration_fit.loc[candidates.index].to_numpy(dtype=float)
        + 0.03 * popularity
        + 0.03 * safety
    )

    candidates["similarity_score"] = similarity_scores
    candidates["final_score"] = final_scores

    # For very short/unclear queries, still return budget-compatible options;
    # similarity remains visible so users can judge relevance.
    relevant = candidates[similarity_scores >= 0.05].copy()
    if relevant.empty:
        print("\nNo strong text match was found; showing the closest budget-compatible options.")
        relevant = candidates.copy()

    relevant = relevant.sort_values("final_score", ascending=False).head(5)
    recommendations = []

    for _, place in relevant.iterrows():
        recommendations.append({
            "destination": place["destination_name"],
            "state": place["state"],
            "budget_min": place["budget_daily_min"],
            "budget_max": place["budget_daily_max"],
            "ideal_days": place["ideal_days"],
            "similarity": round(float(place["similarity_score"]), 3),
            "popularity": place["popularity_score"],
            "safety": place["safety_rating"],
            "final_score": round(float(place["final_score"]), 3),
            "season_match": bool(
                pd.notna(place["best_seasons"])
                and str(season).lower() in str(place["best_seasons"]).lower()
            ),
            "traveler_match": bool(
                pd.notna(place["ideal_for"])
                and str(traveler).replace("_", " ").lower()
                in str(place["ideal_for"]).replace("_", " ").lower()
            ),
        })

    return recommendations


# =========================================================
# 4. USER INPUT AND OUTPUT
# =========================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("WELCOME TO GLOBALTOURAI")
    print("=" * 60)

    query = input("\nWhat do you want to explore? ").strip()

    try:
        budget = float(input("Enter your maximum daily budget (₹): "))
        days = int(input("Enter number of travel days: "))
    except ValueError:
        print("\nInvalid input. Enter a numeric budget and travel days.")
        raise SystemExit(1)

    season = input(
        "Enter preferred season (Winter/Summer/Monsoon): "
    ).strip().capitalize()
    traveler = input(
        "Who are you travelling with? "
        "(Solo/Couple/Friends/Family_with_kids/Family_with_elderly): "
    ).strip()

    valid_seasons = ["Winter", "Summer", "Monsoon"]
    valid_travelers = [
        "Solo", "Couple", "Friends", "Family_with_kids", "Family_with_elderly"
    ]

    if not query:
        print("\nPlease enter a travel interest.")
        raise SystemExit(1)
    if budget <= 0 or days <= 0:
        print("\nBudget and travel days must be greater than zero.")
        raise SystemExit(1)
    if season not in valid_seasons:
        print("\nInvalid season!")
        raise SystemExit(1)
    if traveler not in valid_travelers:
        print("\nInvalid traveler type!")
        raise SystemExit(1)

    print("\nInputs received successfully.")
    print("Calling recommendation engine...")

    results = recommend_destinations(
        query=query, budget=budget, days=days, season=season, traveler=traveler
    )

    print("\n" + "=" * 60)
    print("GLOBALTOURAI RECOMMENDATIONS")
    print("=" * 60)

    if results:
        for rank, place in enumerate(results, start=1):
            print(f"\n{rank}. {place['destination']}, {place['state']}")
            print(
                "   Estimated daily budget: "
                f"₹{place['budget_min']} - ₹{place['budget_max']}"
            )
            print(f"   Ideal trip duration: {place['ideal_days']} days")
            print(f"   Text similarity: {place['similarity']}")
            print(f"   Popularity: {place['popularity']}")
            print(f"   Safety rating: {place['safety']}")
            print(f"   Final score: {place['final_score']}")
            print(f"   Season preference match: {place['season_match']}")
            print(f"   Traveler preference match: {place['traveler_match']}")
    else:
        print("No recommendations available for these inputs.")

    print("\nNumber of results:", len(results))
