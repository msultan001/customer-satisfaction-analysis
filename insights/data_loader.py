from database.db_connection import get_connection
import pandas as pd
import os
from .visualizer import generate_wordcloud, plot_rating_distribution, plot_sentiment_distribution

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
CSV_PATH = os.path.join(BASE_DIR, "data", "cleaned_themed_reviews.csv")
REPORT_PATH = os.path.join(BASE_DIR, "outputs", "bank_insights_summary.csv")
os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)


def get_data():
    df = pd.read_csv(CSV_PATH)
    # Normalize bank names and sentiment labels
    df['bank'] = df['bank'].str.strip()
    df['sentiment_label'] = df['sentiment_label'].str.lower()
    return df


def extract_drivers_pain_points(df):
    """
    For each bank, extract at least two satisfaction drivers and two pain points
    along with some supporting metrics (rating and sentiment score averages)
    """
    insights = []

    for bank in df['bank'].unique():
        sub_df = df[df['bank'] == bank]

        # Positive reviews: satisfaction drivers
        pos_reviews = sub_df[sub_df['sentiment_label'] == 'positive']['cleaned_review'].tolist()
        drivers = pos_reviews[:3] if len(pos_reviews) >= 3 else pos_reviews

        # Negative reviews: pain points
        neg_reviews = sub_df[sub_df['sentiment_label'] == 'negative']['cleaned_review'].tolist()
        pains = neg_reviews[:3] if len(neg_reviews) >= 3 else neg_reviews

        # Supporting metrics
        avg_rating = sub_df['rating'].mean().round(2)
        avg_sentiment = sub_df['sentiment_score'].mean().round(2)

        # Concrete actionable recommendations
        recommendations = []
        if drivers:
            recommendations.append(f"Leverage strengths: {drivers[0]} / {drivers[1] if len(drivers) > 1 else ''}")
        if pains:
            recommendations.append(f"Address pain points: {pains[0]} / {pains[1] if len(pains) > 1 else ''}")

        insights.append({
            "bank": bank,
            "satisfaction_drivers": "; ".join(drivers) if drivers else "N/A",
            "pain_points": "; ".join(pains) if pains else "N/A",
            "avg_rating": avg_rating,
            "avg_sentiment_score": avg_sentiment,
            "actionable_recommendations": "; ".join(recommendations)
        })

    return pd.DataFrame(insights)


def generate_report(df_insights):
    """Save the insights summary to CSV"""
    df_insights.to_csv(REPORT_PATH, index=False)
    print(f"Bank insights summary saved to {REPORT_PATH}")


if __name__ == '__main__':
    df = get_data()

    # Generate plots
    generate_wordcloud(df)
    plot_rating_distribution(df)
    plot_sentiment_distribution(df)

    # Extract drivers, pain points, and recommendations
    df_insights = extract_drivers_pain_points(df)

    # Save report
    generate_report(df_insights)

    # Optional: print summary
    print(df_insights)
