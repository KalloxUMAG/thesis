from datetime import datetime

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from scripts.stringdb import download, get_uniprot_ids, remove_not_found, string_to_db, load_interactions_to_db

default_args = {
    'owner': 'Kallox',
    'start_date': datetime(2023, 2, 3, 21, 0, 0)
}

with DAG(dag_id='download_string', default_args=default_args, schedule='@monthly') as dag:
    start = EmptyOperator(task_id='start')

    get_antibodies_ids = PythonOperator(task_id='get_uniprot_ids', python_callable=get_uniprot_ids)

    download_interactions = PythonOperator(task_id='download_interactions', python_callable=download)

    convert_stringid_to_databaseid = PythonOperator(task_id='convert_stringid_to_databaseid', python_callable=string_to_db)

    remove_not_found_ids = PythonOperator(task_id='remove_not_found_ids', python_callable=remove_not_found)

    load_interactions = PythonOperator(task_id='load_interactions', python_callable=load_interactions_to_db)

    end = EmptyOperator(task_id='end')

    start >> get_antibodies_ids >> download_interactions >> convert_stringid_to_databaseid >> remove_not_found_ids >> load_interactions >> end
