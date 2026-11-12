
import requests
import streamlit as st
import os

API_URL = os.getenv("http://127.0.0.1:8000/recommend")

st.set_page_config(
    page_title="GlobalTourAI",
    page_icon="🌍",
    layout="wide",
)

# ---------- Styling ----------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f3f8ff, #f7f4ff);
    }
    .hero {
        padding: 28px;
        border-radius: 18px;
        background: linear-gradient(120deg, #123c69, #2a6f97);
        color: white;
        margin-bottom: 22px;
    }
    .hero h1 {
        color: white;
        font-size: 38px;
    }
    .hero p {
        color: white;
        font-size: 17px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown(
    """
    <div class="hero">
        <h1>🌍 GlobalTourAI</h1>
        <p>Your AI-powered guide to exploring incredible India.</p>
        <p>Discover destinations based on your interests, budget, and travel style.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("✈️ Plan your next trip")
st.write("Tell us what kind of experience you are looking for.")

# ---------- Input form ----------
with st.form("travel_preferences"):
    query = st.text_input(
        "What would you like to explore?",
        placeholder="Example: forts, temples, beaches, mountains, local culture",
    )

    col1, col2 = st.columns(2)

    with col1:
        budget = st.number_input(
            "Daily budget (₹)",
            min_value=500,
            max_value=100000,
            value=3000,
            step=500,
        )

        days = st.number_input(
            "Trip duration (days)",
            min_value=1,
            max_value=60,
            value=5,
            step=1,
        )

    with col2:
        season = st.selectbox(
            "Travel season",
            ["Winter", "Summer", "Monsoon"],
        )

        traveler = st.selectbox(
            "Who are you travelling with?",
            [
                "Solo",
                "Couple",
                "Friends",
                "Family_with_kids",
                "Family_with_elderly",
            ],
            format_func=lambda value: value.replace("_", " "),
        )

    submitted = st.form_submit_button(
        "🔎 Find My Destinations",
        use_container_width=True,
    )

# ---------- Recommendations ----------
if submitted:
    if not query.strip():
        st.warning("Please enter your travel interests first.")
    else:
        payload = {
            "query": query.strip(),
            "budget": budget,
            "days": days,
            "season": season,
            "traveler": traveler,
        }

        try:
            with st.spinner("Finding destinations for you..."):
                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=120,
                )
                response.raise_for_status()
                data = response.json()

            recommendations = data.get("recommendations", [])

            st.divider()
            st.subheader("✨ Your Recommended Destinations")
            st.caption(
                f"Found {len(recommendations)} destination(s) "
                f"for your travel preferences."
            )

            if not recommendations:
                st.info(
                    "No destinations matched this search. "
                    "Try different interests or a higher daily budget."
                )
            else:
                for index, destination in enumerate(recommendations, start=1):
                    name = destination.get(
                        "destination", "Unknown destination"
                    )
                    state = destination.get("state", "India")
                    budget_min = destination.get("budget_min")
                    budget_max = destination.get("budget_max")
                    ideal_days = destination.get("ideal_days")
                    similarity = destination.get("similarity")
                    final_score = destination.get("final_score")
                    season_match = destination.get("season_match")
                    traveler_match = destination.get("traveler_match")

                    with st.container(border=True):
                        st.markdown(
                            f"### {index}. {name}, {state}"
                        )

                        left, middle, right = st.columns(3)

                        with left:
                            if (
                                budget_min is not None
                                and budget_max is not None
                            ):
                                st.metric(
                                    "Estimated daily budget",
                                    f"₹{budget_min:,.0f}–₹{budget_max:,.0f}",
                                )
                            else:
                                st.write("Daily budget: Not available")

                        with middle:
                            if ideal_days is not None:
                                st.metric(
                                    "Ideal trip duration",
                                    f"{ideal_days} days",
                                )

                        with right:
                            if final_score is not None:
                                st.metric(
                                    "Recommendation score",
                                    f"{final_score:.3f}",
                                )

                        if similarity is not None:
                            st.write(
                                f"**Interest similarity score:** "
                                f"{similarity:.3f}"
                            )

                        st.write(
                            f"**Season match:** "
                            f"{'Yes' if season_match else 'No'}"
                        )
                        st.write(
                            f"**Traveler preference match:** "
                            f"{'Yes' if traveler_match else 'No'}"
                        )

            st.caption(
                "Budget figures are dataset estimates, not live prices. "
                "Recommendation scores are ranking scores, not probabilities."
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to the GlobalTourAI API. "
                "Please ensure FastAPI is running on port 8000."
            )
        except requests.exceptions.Timeout:
            st.error(
                "The recommendation request took too long. "
                "Please try again."
            )
        except requests.exceptions.RequestException as error:
            st.error(f"API request failed: {error}")
        except (ValueError, TypeError, KeyError) as error:
            st.error(
                f"Could not process the recommendation response: {error}"
            )

st.divider()
st.caption(
    "GlobalTourAI | Machine Learning Mini-Project | "
    "Content-based destination recommendation"
)
