import pandas as pd
from datetime import datetime
import os

# Function to generate datetime objects for consistent testing
def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def create_and_save_test_data(year, month):
    # This is the same data from your Q3 unit test, extended slightly for more robustness
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df_input = pd.DataFrame(data, columns=columns)

    # --- S3 Configuration for saving ---
    S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL', 'http://localhost:4566') # Default to Localstack
    
    # Define the input file path for January 2023
    # This should match how q45_batch.py expects the input file
    input_file_pattern = os.getenv('INPUT_FILE_PATTERN', 's3://nyc-duration/in/{year:04d}-{month:02d}.parquet')
    input_file = input_file_pattern.format(year=year, month=month)

    options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL
        }
    }

    print(f"Saving test data to: {input_file} using endpoint: {S3_ENDPOINT_URL}")

    try:
        df_input.to_parquet(
            input_file,
            engine='pyarrow',
            compression=None,
            index=False,
            storage_options=options
        )
        print("Test data saved successfully!")
    except Exception as e:
        print(f"Error saving test data: {e}")

if __name__ == "__main__":
    # We will pretend this is data for January 2023
    create_and_save_test_data(2023, 1)