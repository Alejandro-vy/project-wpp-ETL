from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Define tu DAG
with DAG(
    dag_id='wpp_etl_dag',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,   # Manual
    catchup=False
) as dag:

    # Task: Ejecutar tu script de extracción
    extract_population = BashOperator(
        task_id='extract_population',
        bash_command='python /opt/airflow/scripts/extract_wpp.py'
    )

    extract_population

