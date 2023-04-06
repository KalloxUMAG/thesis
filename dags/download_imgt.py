from datetime import datetime

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from scripts.imgt import download, remove_antibodies, load_antibodies_to_db

default_args = {
    'owner': 'Kallox',
    'start_date': datetime(2022, 11, 3, 21, 20, 0)
}

with DAG(dag_id='download_imgt', default_args=default_args, schedule='@monthly') as dag:
    start = EmptyOperator(task_id='start')

    download_files = PythonOperator(task_id='download_files', python_callable=download)

    remove_existing_antibodies = PythonOperator(task_id='remove_existing_antibodies', python_callable=remove_antibodies)

    load_antibodies = PythonOperator(task_id='load_antibodies', python_callable=load_antibodies_to_db)

    end = EmptyOperator(task_id='end')

    start >> download_files >> remove_existing_antibodies >> load_antibodies >> end
    