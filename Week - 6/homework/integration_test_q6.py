import os
import sys
import pickle
import pandas as pd
from datetime import datetime
from q45_batch import prepare_data, get_input_path, get_output_path

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def create_test_dataframe():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),     # 9 mins
        (1, 1, dt(1, 2), dt(1, 10)),           # 8 mins
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),  # 59 mins
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      # 1441 mins -> filtered
    ]
    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    return pd.DataFrame(data, columns=columns)

def create_and_save_input(year, month, df_input, s3_endpoint):
    input_file = get_input_path(year, month)
    options = {
        'client_kwargs': {
            'endpoint_url': s3_endpoint
        }
    }
    df_input.to_parquet(
        input_file,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options
    )
    print(f"Test input data written to {input_file}")

def read_output_and_validate(year, month, df_input, s3_endpoint):
    output_file = get_output_path(year, month)
    options = {
        'client_kwargs': {
            'endpoint_url': s3_endpoint
        }
    }

    df_result = pd.read_parquet(output_file, storage_options=options)
    predicted_sum = df_result['predicted_duration'].sum()
    print(f"✅ Predicted duration sum from output file: {predicted_sum:.2f}")

    # --- Compute expected predictions ---
    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)

    categorical = ['PULocationID', 'DOLocationID']
    df_prepared = prepare_data(df_input, categorical)

    dicts = df_prepared[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    expected_preds = lr.predict(X_val)

    expected_sum = expected_preds.sum()
    print(f"✅ Expected predicted duration sum (from model): {expected_sum:.2f}")

    assert abs(predicted_sum - expected_sum) < 1e-6, "Predicted sum doesn't match expected"

if __name__ == "__main__":
    year, month = 2023, 1
    s3_endpoint = os.getenv('S3_ENDPOINT_URL', 'http://localhost:4566')

    df_input = create_test_dataframe()
    create_and_save_input(year, month, df_input, s3_endpoint)

    # Run your batch job (replace with subprocess.run if you prefer)
    exit_code = os.system(f'python q45_batch.py {year} {month}')
    assert exit_code == 0, "Batch job failed"

    read_output_and_validate(year, month, df_input, s3_endpoint)
