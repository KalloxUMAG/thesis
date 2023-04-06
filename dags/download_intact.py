from datetime import datetime

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from scripts.intact import download, get_uniprot_ids, join_interactions, load_interactions_to_db

default_args = {
    'owner': 'Kallox',
    'start_date': datetime(2023, 1, 3, 21, 0, 0)
}

with DAG(dag_id='download_intact', default_args=default_args, schedule='@monthly') as dag:
    start = EmptyOperator(task_id='start')

    get_antibodies_ids = PythonOperator(task_id='get_uniprot_ids', python_callable=get_uniprot_ids)

    download_files = PythonOperator(task_id='download_files', python_callable=download)

    join_files = PythonOperator(task_id='join_files', python_callable=join_interactions)

    load_interactions = PythonOperator(task_id='load_interactions', python_callable=load_interactions_to_db)

    end = EmptyOperator(task_id='end')

    start >> get_antibodies_ids >> download_files >> join_files >> load_interactions >> end
