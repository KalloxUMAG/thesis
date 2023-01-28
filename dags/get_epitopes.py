from datetime import datetime

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from scripts.hivmidb.extract_epitopes import extract_epitopes
from scripts.iedb.drop_columns import drop_columns_epitopes
from scripts.vdjdb.extract_epitopes import extract_epitopes as vdjdb_extract_epitopes
from scripts.epitopes.join_files import join_files

default_args = {
    'owner': 'Kallox',
    'start_date': datetime(2022, 11, 3, 21, 0, 0)
}

with DAG(dag_id='get_epitopes', default_args=default_args, schedule='@monthly') as dag:
    
    start = EmptyOperator(task_id='start')

    hiv_midb = PythonOperator(task_id='hiv_midb', python_callable=extract_epitopes)

    iedb = PythonOperator(task_id='iedb', python_callable=drop_columns_epitopes)

    vdjdb = PythonOperator(task_id='vdjdb', python_callable=vdjdb_extract_epitopes)

    join_epitopes = PythonOperator(task_id='join_epitopes', python_callable=join_files)

    load_to_database = EmptyOperator(task_id='load_to_database')

    end = EmptyOperator(task_id='end')

    start >> hiv_midb >> iedb >> vdjdb >> join_epitopes >> load_to_database >> end
