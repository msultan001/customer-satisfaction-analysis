import os
import unittest
import pandas as pd
from datetime import datetime
from unittest.mock import patch

# Import functions from your modules
from database.create_schema import create_tables
from database.insert_data_and_simple_query import insert_data, CSV_PATH  # CSV_PATH will be patched
from database.db_connection import get_connection

class TestDatabaseOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure that schema is set up before tests run.
        create_tables()
    
    def setUp(self):
        # Clear tables before each test.
        self.conn = get_connection()
        with self.conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE reviews RESTART IDENTITY CASCADE;")
            cur.execute("TRUNCATE TABLE bank RESTART IDENTITY CASCADE;")
            # Insert dummy bank records manually (as expected)
            cur.execute("INSERT INTO bank (bankname, appname) VALUES ('CBE', 'CBE Mobile'), ('Dashen', 'Dashen Mobile'), ('BoA', 'BoA Mobile')")
        self.conn.commit()
    def test_insert_data(self):
        test_csv_path = "tests/test_data.csv"
    def tearDown(self):
        with self.conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE reviews RESTART IDENTITY CASCADE;")
            cur.execute("TRUNCATE TABLE bank RESTART IDENTITY CASCADE;")
        self.conn.commit()
        self.conn.close()
    
    def test_create_tables_exist(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT to_regclass('public.bank');")
            bank_table = cur.fetchone()[0]
            cur.execute("SELECT to_regclass('public.reviews');")
            reviews_table = cur.fetchone()[0]
        self.assertEqual(bank_table, 'bank')
        self.assertEqual(reviews_table, 'reviews')
    
    def test_insert_data(self):
        # Create a temporary CSV file to simulate cleaned_themed_reviews.csv
        test_df = pd.DataFrame({
            "bank": ["CBE", "Dashen", "BoA"],
            "cleaned_review": [
                "Great app experience.",
                "The interface can be improved.",
                "Frequent crashes during usage."
            ],
            "rating": [5, 3, 1],
            "date": [datetime.now().strftime("%Y-%m-%d")] * 3,
            "sentiment_label": ["positive", "neutral", "negative"],
            "sentiment_score": [0.95, 0.50, 0.20],
            "source": ["Google Play"] * 3
        })

        # Write test CSV file in a temporary location, then patch CSV_PATH to point to it.
        test_csv_path = os.path.join(os.path.dirname(CSV_PATH), "test_cleaned_themed_reviews.csv")
        test_df.to_csv(test_csv_path, index=False)

        with patch('insert_data.CSV_PATH', test_csv_path):
            insert_data()

        # Verify that records were inserted into reviews table.
        with self.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM reviews;")
            count = cur.fetchone()[0]
        self.assertEqual(count, 3)

        # Cleanup test CSV file
        if os.path.exists(test_csv_path):
            os.remove(test_csv_path)

if __name__ == '__main__':
    unittest.main()