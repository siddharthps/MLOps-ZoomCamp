import datetime
import psycopg
from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric

def execute(reference_data, raw_data, model):
    begin = datetime.datetime(2025, 1, 1, 0, 0)
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

    with psycopg.connect("host=db port=5432 dbname=test user=postgres password=example", autocommit=True) as conn:
        for i in range(27):  # Loop over 27 days
            current_data = raw_data[
                (raw_data.lpep_pickup_datetime >= (begin + datetime.timedelta(i))) &
                (raw_data.lpep_pickup_datetime < (begin + datetime.timedelta(i + 1)))
            ]
            current_data['prediction'] = model.predict(current_data[num_features + cat_features].fillna(0))

            report.run(reference_data=reference_data, current_data=current_data, column_mapping=column_mapping)
            result = report.as_dict()

            prediction_drift = result['metrics'][0]['result']['drift_score']
            num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
            share_missing_values = result['metrics'][2]['result']['current']['share_of_missing_values']

            with conn.cursor() as curr:
                curr.execute(
                    """
                    insert into dummy_metrics(timestamp, prediction_drift, num_drifted_columns, share_missing_values)
                    values (%s, %s, %s, %s)
                    """,
                    (begin + datetime.timedelta(i), prediction_drift, num_drifted_columns, share_missing_values)
                )
