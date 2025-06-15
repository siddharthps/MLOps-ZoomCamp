import pickle
import pandas as pd
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--year', type=int, required=True, help='Year')
parser.add_argument('--month', type=int, required=True, help='Month')

args = parser.parse_args()
year = args.year
month = args.month

with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet'
df = read_data(input_file)

dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)

mean_pred = np.mean(y_pred)
std_pred = np.std(y_pred)

print(f"Mean predicted duration: {mean_pred:.2f} minutes")
print(f"Standard deviation of predicted duration: {std_pred:.2f} minutes")


#Preparing the output

df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')


df_result = pd.DataFrame()
df_result['ride_id'] = df['ride_id']
df_result['predicted_duration'] = y_pred


output_file = f'predictions_{year}_{month:02d}.parquet'

df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)


