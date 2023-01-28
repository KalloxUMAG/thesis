from datetime import datetime

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from scripts.intact.download import download as intact_download
from scripts.intact.get_uniprot_ids import get_uniprot_ids as intact_get_uniprot_ids

from scripts.string.download import download as string_download
from scripts.string.get_uniprot_ids import get_uniprot_ids as string_get_uniprot_ids
from scripts.string.string_to_db import string_to_db
from scripts.string.remove_not_found import remove_not_found

from scripts.interactions.join_interactions import join_interactions as join_files


def load_intact_taskgroup(group_id):
    with TaskGroup(group_id=group_id) as taskgroup:

        start = EmptyOperator(task_id='start')

        get_uniprot_ids = PythonOperator(task_id='get_uniprot_ids', python_callable=intact_get_uniprot_ids)

        download_files = PythonOperator(task_id='download_files', python_callable=intact_download)

        end = EmptyOperator(task_id='end')

        start >> get_uniprot_ids >> download_files >> end

    return taskgroup


def load_string_taskgroup(group_id):
    with TaskGroup(group_id=group_id) as taskgroup:

        start = EmptyOperator(task_id='start')

        get_uniprot_ids = PythonOperator(task_id='string_get_uniprot_ids', python_callable=string_get_uniprot_ids)

        download_files = PythonOperator(task_id='string_download_files', python_callable=string_download)

        convert_string_ids = PythonOperator(task_id='convert_string_ids', python_callable=string_to_db)

        remove_id_not_found = PythonOperator(task_id='string_remove_id_not_found', python_callable=remove_not_found)

        end = EmptyOperator(task_id='end')

        start >> get_uniprot_ids >> download_files >> convert_string_ids >> remove_id_not_found >> end

    return taskgroup


default_args = {
    'owner': 'Kallox',
    'start_date': datetime(2022, 11, 3, 21, 0, 0)
}

with DAG(dag_id='get_interactions', default_args=default_args, schedule='@monthly') as dag:
    
    start = EmptyOperator(task_id='start')

    intact = load_intact_taskgroup('intact')

    string = load_string_taskgroup('string')

    join_interactions = PythonOperator(task_id='join_interactions', python_callable=join_files)

    load_to_database = EmptyOperator(task_id='load_to_database')

    end = EmptyOperator(task_id='end')

    start >> [string, intact] >> join_interactions >> load_to_database >> end
