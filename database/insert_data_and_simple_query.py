import pandas as pd
import psycopg2
import sys
import os
from .db_connection import get_connection
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "query_logs.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

CSV_PATH = os.path.join(BASE_DIR, "data", "cleaned_themed_reviews.csv")

def insert_data():
    df = pd.read_csv(CSV_PATH)

    bank_map = {
        "BoA": 3,
        "Dashen": 2,
        "CBE": 1
    }

    try:
        connection = get_connection()
        cursor = connection.cursor()

        for _, row in df.iterrows():
            bank_id = bank_map.get(row["bank"], 1)

            cursor.execute(
                """
                INSERT INTO reviews 
                (bank_id, review_text, rating, review_date, sentimentlabel, sentimentscore, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    bank_id,
                    row["cleaned_review"],
                    row["rating"],
                    pd.to_datetime(row["date"]),
                    row["sentiment_label"],
                    row["sentiment_score"],
                    row["source"]
                )
            )
        cursor.execute(
            """
            Select b.bankname, COUNT(*) from bank b join reviews r on b.bank_id = r.bank_id
            GROUP BY b.bankname
            """
        )
        result = cursor.fetchall()
        logger.info(result)
        connection.commit()

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    insert_data()
