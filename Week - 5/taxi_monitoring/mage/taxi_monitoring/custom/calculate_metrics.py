if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(*args, **kwargs):
    import pandas as pd
    import datetime
    import joblib
    import psycopg
    from evidently.report import Report
    from evidently import ColumnMapping
    from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric

    # Load reference data & model
    reference_data = pd.read_parquet('data/reference.parquet')
    raw_data = pd.read_parquet('data/green_tripdata_2025-01.parquet')
    model = joblib.load('models/lin_reg.bin')

    num_features = ['passenger_count', 'trip_distance', 'fare_amount', 'total_amount']
    cat_features = ['PULocationID', 'DOLocationID']

    column_mapping = ColumnMapping(
        prediction='prediction',
        numerical_features=num_features,
        categorical_features=cat_features,
        target=None
    )

    report = Report(metrics=[
        ColumnDriftMetric(column_name='prediction'),
        DatasetDriftMetric(),
        DatasetMissingValuesMetric()
    ])

    begin = datetime.datetime(2025, 1, 1)

    # Open connection
    with psycopg.connect("host=db port=5432 dbname=test user=postgres password=example", autocommit=True) as conn:
        for i in range(27):  # 27 days
            current_data = raw_data[
                (raw_data.lpep_pickup_datetime >= (begin + datetime.timedelta(i))) &
                (raw_data.lpep_pickup_datetime < (begin + datetime.timedelta(i + 1)))
            ]

            current_data['prediction'] = model.predict(
                current_data[num_features + cat_features].fillna(0)
            )

            report.run(reference_data=reference_data, current_data=current_data, column_mapping=column_mapping)
            result = report.as_dict()

            prediction_drift = result['metrics'][0]['result']['drift_score']
            num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
            share_missing_values = result['metrics'][2]['result']['current']['share_of_missing_values']

            with conn.cursor() as curr:
                curr.execute(
                    """
                    INSERT INTO dummy_metrics(timestamp, prediction_drift, num_drifted_columns, share_missing_values)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (begin + datetime.timedelta(i), prediction_drift, num_drifted_columns, share_missing_values)
                )

    return "Metrics inserted for 27 days"
