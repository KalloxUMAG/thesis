import os.path
from datetime import datetime

from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable

from scripts.catnap import download, extract, remove_antibodies, remove_antigens, load_antigens_to_db, load_antibodies_to_db

default_args = {
    'owner': 'admin',
    'start_date': datetime(2022, 11, 2, 18, 0, 0,)
}

with DAG(dag_id='download_catnap', default_args=default_args, schedule='0 0 8 * *') as dag:
    start = EmptyOperator(task_id='start')

    download_files = PythonOperator(task_id='download_files', python_callable=download)

    extract_files = PythonOperator(task_id='extract_files', python_callable=extract)

    remove_existing_antibodies = PythonOperator(task_id='remove_existing_antibodies', python_callable=remove_antibodies)

    remove_existing_antigens = PythonOperator(task_id='remove_existing_antigens', python_callable=remove_antigens)

    load_antibodies = PythonOperator(task_id='load_antibodies', python_callable=load_antibodies_to_db)
    
    load_antigens = PythonOperator(task_id='load_antigens', python_callable=load_antigens_to_db)

    end = EmptyOperator(task_id='end')

    start >> download_files >> extract_files >> remove_existing_antibodies >> remove_existing_antigens >> load_antibodies >> load_antigens >> end
