import pandas as pd
import joblib

def execute():
    reference_data = pd.read_parquet('data/reference.parquet')
    raw_data = pd.read_parquet('data/green_tripdata_2025-01.parquet')
    with open('models/lin_reg.bin', 'rb') as f_in:
        model = joblib.load(f_in)

    return reference_data, raw_data, model
