from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'retries': 1,
}

with DAG(
    dag_id='wpp_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for World Population Prospects data',
    schedule_interval=None,  # Ponlo None para lanzarlo manual al inicio
    start_date=days_ago(1),
    catchup=False,
    tags=['ETL', 'wpp', 'population'],
) as dag:

    extract = BashOperator(
        task_id='extract_data',
        bash_command='python /opt/airflow/scripts/extract_wpp.py'
    )

    transform = BashOperator(
        task_id='transform_data',
        bash_command='python /opt/airflow/scripts/transform_wpp.py'
    )

    load = BashOperator(
        task_id='load_data',
        bash_command='python /opt/airflow/scripts/load_wpp.py'
    )

    extract >> transform >> load



