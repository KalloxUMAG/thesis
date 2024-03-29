from datetime import datetime

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from scripts.vdjdb import download, extract_antibodies, extract_epitopes, remove_antibodies, remove_epitopes, load_antibodies_to_db, load_epitopes_to_db

default_args = {
    'owner': 'Kallox',
    'start_date': datetime(2023, 2, 20, 21, 0, 0)
}

with DAG(dag_id='download_vdjdb', default_args=default_args, schedule='@monthly') as dag:
    start = EmptyOperator(task_id='start')

    download_files = PythonOperator(task_id='download_files', python_callable=download)

    get_epitopes = PythonOperator(task_id='get_epitopes', python_callable=extract_epitopes)

    get_antibodies = PythonOperator(task_id='get_antibodies', python_callable=extract_antibodies)

    remove_existing_antibodies = PythonOperator(task_id='remove_existing_antibodies', python_callable=remove_antibodies)

    remove_existing_epitopes = PythonOperator(task_id='remove_existing_epitopes', python_callable=remove_epitopes)

    load_antibodies = PythonOperator(task_id='load_antibodies', python_callable=load_antibodies_to_db)

    load_epitopes = PythonOperator(task_id='load_epitopes', python_callable=load_antibodies_to_db)

    end = EmptyOperator(task_id='end')

    start >> download_files >> get_antibodies >> get_epitopes >> remove_existing_antibodies >> remove_existing_epitopes >> load_antibodies >> load_epitopes >> end
