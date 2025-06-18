if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(*args, **kwargs):
    import psycopg

    # Define table statement at the top so it's accessible in both blocks
    create_table_statement = """
    drop table if exists dummy_metrics;
    create table dummy_metrics(
        timestamp timestamp,
        prediction_drift float,
        num_drifted_columns integer,
        share_missing_values float
    )
    """

    # Create DB if it doesn't exist
    with psycopg.connect("host=db port=5432 user=postgres password=example", autocommit=True) as conn:
        res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
        if len(res.fetchall()) == 0:
            conn.execute("create database test;")

    # Create table in the test DB
    with psycopg.connect("host=db port=5432 dbname=test user=postgres password=example") as conn:
        conn.execute(create_table_statement)

    return "Database Ready"

      
