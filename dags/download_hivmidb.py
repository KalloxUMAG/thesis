from datetime import datetime

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from scripts.hivmidb.download import download
from scripts.hivmidb.join_antibodies import join_antibodies

default_args = {
    'owner': 'Kallox',
    'start_date': datetime(2022, 11, 3, 21, 0, 0)
}

with DAG(dag_id='download_hivmidb', default_args=default_args, schedule='@monthly') as dag:
    
    start = EmptyOperator(task_id='start')

    download_files = PythonOperator(task_id='download', python_callable=download)

    join_files = PythonOperator(task_id='join_files', python_callable=join_antibodies)

    end = EmptyOperator(task_id='end')

    start >> download_files >> join_files >> end
