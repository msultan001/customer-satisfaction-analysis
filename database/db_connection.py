import psycopg2
import pandas as pd
def get_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",        # Database host
            database="customer_satisfaction", # Name of your database
            user="postgres",    # PostgreSQL username
            password="1234",# PostgreSQL password
            port=5432                # Default PostgreSQL port
        )
        return connection
    except psycopg2.Error as e:
        print(f'Error connecting to PostgresSQL: {e}')
        return None
    
def insert_data():
    pass
    
insert_data()
        