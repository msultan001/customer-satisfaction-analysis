from database.db_connection import get_connection
import pandas as pd
import psycopg2
import sys
import os
from .visualizer import generate_wordcloud, plot_rating_distribution, plot_sentiment_distribution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # two levels up
CSV_PATH = os.path.join(BASE_DIR, "data", "cleaned_themed_reviews.csv")
def get_data():
    df = pd.read_csv(CSV_PATH)
    return df




def extract_drivers_pain_points(df):
    drivers, pains = {}, {}

    for bank in df['bank'].unique():
        sub_df = df[df['bank'] == bank]

        # Normalize sentiment labels just in case
        sub_df['sentiment_label'] = sub_df['sentiment_label'].str.lower()

        # Extract positive reviews
        pos_reviews = sub_df[sub_df['sentiment_label'] == 'positive']['cleaned_review']
        if len(pos_reviews) >= 3:
            drivers[bank] = pos_reviews.sample(3).tolist()
        else:
            drivers[bank] = pos_reviews.sample(len(pos_reviews)).tolist() if not pos_reviews.empty else []

        # Extract negative reviews
        neg_reviews = sub_df[sub_df['sentiment_label'] == 'negative']['cleaned_review']
        if len(neg_reviews) >= 3:
            pains[bank] = neg_reviews.sample(3).tolist()
        else:
            pains[bank] = neg_reviews.sample(len(neg_reviews)).tolist() if not neg_reviews.empty else []

    return drivers, pains

def compare_banks(df):
    comparison = df.groupby('bank_name').agg({
        'rating': ['mean'],
        'sentiment_score': ['mean']
    }).round(2)
    return comparison
if __name__ == '__main__':
    df = get_data()
    generate_wordcloud(df)
    plot_rating_distribution(df)
    plot_sentiment_distribution(df)
    