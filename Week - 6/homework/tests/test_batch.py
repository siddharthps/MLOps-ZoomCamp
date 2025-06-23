import pandas as pd
from datetime import datetime
from q3_batch import prepare_data


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def test_prepare_data():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),      # 9 mins, missing locations -> kept
        (1, 1, dt(1, 2), dt(1, 10)),            # 8 mins, valid -> kept
        (1, None, dt(1, 2, 0), dt(1, 3, 0)),    # 1 min, missing DOLocationID -> kept (FIXED LINE)
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),       # 1441 mins -> filtered out
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)

    categorical = ['PULocationID', 'DOLocationID']
    actual = prepare_data(df, categorical)

    expected_data = [
        ('-1', '-1', 9.0),
        ('1', '1', 8.0),
        ('1', '-1', 1.0), # Updated expected duration for the fixed line
    ]
    expected_df = pd.DataFrame(expected_data, columns=['PULocationID', 'DOLocationID', 'duration'])

    pd.testing.assert_frame_equal(
        actual[['PULocationID', 'DOLocationID', 'duration']].reset_index(drop=True),
        expected_df
    )