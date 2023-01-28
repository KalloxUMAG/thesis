from datetime import datetime

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from scripts.intact.download import download
from scripts.intact.get_uniprot_ids import get_uniprot_ids

default_args = {
    'owner': 'Kallox',
    'start_date': datetime(2022, 11, 3, 21, 0, 0)
}

with DAG(dag_id='download_intact', default_args=default_args, schedule='@monthly') as dag:
    start = EmptyOperator(task_id='start')

    get_uniprot_ids = PythonOperator(task_id='get_uniprot_ids', python_callable=get_uniprot_ids)

    download_files = PythonOperator(task_id='download_files', python_callable=download)

    end = EmptyOperator(task_id='end')

    start >> get_uniprot_ids >> download_files >> end
