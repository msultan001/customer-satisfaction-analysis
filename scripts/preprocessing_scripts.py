import pandas as pd
from google_play_scraper import reviews
from tqdm import tqdm
import csv
import logging

# Setup logging
logging.basicConfig(
    filename='logs/preprocessing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class DataSetLoadAndPreprocess:

    def accumulate_reviews(self, app_id=None, target=400):
        """
        Fetch Google Play Store reviews until a target count of unique reviews is reached.
        """
        seen_ids = set()
        all_reviews = []
        while len(all_reviews) < target:
            bank_reviews, _ = reviews(app_id=app_id, count=target, lang='en', country='us')
            for review in bank_reviews:
                if review.get('reviewId') not in seen_ids:
                    seen_ids.add(review.get('reviewId'))
                    if len(all_reviews) < target:
                        all_reviews.append(review)
                    else:
                        break
        logging.info(f"Accumulated {len(all_reviews)} unique reviews for app {app_id}")
        return all_reviews

    def preprocessing_data(self, bank_name=None, data_frame=None):
        """
        Standardize review data: rename columns, add metadata, normalize dates,
        remove duplicates, and validate missing values.
        """
        # Rename columns
        data_frame = data_frame.rename(columns={'content': 'review', 'at': 'date', 'score': 'rating'})

        # Add metadata
        data_frame['bank'] = bank_name
        data_frame['source'] = 'Google Play'

        # Normalize date
        data_frame['date'] = pd.to_datetime(data_frame['date']).dt.date

        # Remove duplicates based on review text, date, and rating (or reviewId if available)
        before_rows = data_frame.shape[0]
        if 'reviewId' in data_frame.columns:
            data_frame = data_frame.drop_duplicates(subset=['reviewId'])
        else:
            data_frame = data_frame.drop_duplicates(subset=['review', 'date', 'rating'])
        after_rows = data_frame.shape[0]
        dropped = before_rows - after_rows
        logging.info(f"Removed {dropped} duplicate rows for bank {bank_name}")

        # Check required fields for <5% missing values
        required_cols = ['review', 'rating', 'date', 'bank', 'source']
        for col in required_cols:
            missing_pct = data_frame[col].isna().sum() / data_frame.shape[0]
            if missing_pct > 0.05:
                logging.warning(f"{col} has {missing_pct:.2%} missing values")
            # Optional assertion to enforce threshold
            assert missing_pct <= 0.05, f"{col} exceeds 5% missing values"

        return data_frame

    def export_to_csv(self, file_path=None, columns=None, data=None):
        """
        Export DataFrame to CSV with progress bar.
        """
        if columns is None:
            columns = ['review', 'rating', 'source', 'date', 'bank']

        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columns)

            for _, row in tqdm(data[columns].iterrows(), total=len(data)):
                writer.writerow(row)

        logging.info(f"Exported {len(data)} rows to {file_path}")
