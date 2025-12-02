from .db_connection import get_connection
import psycopg2
import pandas as pd

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS bank (
                bank_id SERIAL PRIMARY KEY,
                bankname TEXT,
                appname TEXT
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reviews(
                reviewId SERIAL PRIMARY KEY,
                bank_id INTEGER REFERENCES bank(bank_id),
                review_text TEXT,
                rating FLOAT,
                review_date DATE,
                sentimentlabel TEXT,
                sentimentscore FLOAT,
                source TEXT
            )
            """
        )
        connection.commit()

    except psycopg2.Error as e:
        print(f"Error occurred: {e}")

    finally:
        cursor.close()
        connection.close()
        
if __name__ == '__main__':
    create_tables()
