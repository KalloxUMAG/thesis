from datetime import datetime

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from scripts.hivmidb import download, extract_epitopes, remove_epitopes

default_args = {
    'owner': 'Kallox',
    'start_date': datetime(2022, 11, 3, 21, 0, 0)
}

with DAG(dag_id='download_hivmidb', default_args=default_args, schedule='@monthly') as dag:
    
    start = EmptyOperator(task_id='start')

    download_files = PythonOperator(task_id='download', python_callable=download)

    epitopes = PythonOperator(task_id='epitopes', python_callable=extract_epitopes)

    remove_existing_epitopes = PythonOperator(task_id='remove_existing_epitopes', python_callable=remove_epitopes)

    end = EmptyOperator(task_id='end')

    start >> download_files >> epitopes >> remove_existing_epitopes >> end
