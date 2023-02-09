from datetime import datetime

from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from scripts.covabdab import download, extract

default_args = {
    'owner': 'Kallox',
    'start_date': datetime(2022, 11, 2, 19, 40, 0)
}

with DAG(dag_id='download_covabdab', default_args=default_args, schedule='@monthly') as dag:
    start = EmptyOperator(task_id='start')

    download_files = PythonOperator(task_id='download_files', python_callable=download)

    extract_files = PythonOperator(task_id="extract_files", python_callable=extract)

    end = EmptyOperator(task_id='end')

    start >> download_files >> extract_files >> end
