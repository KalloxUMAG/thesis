from datetime import datetime

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from scripts.catnap.extract import extract as extract_catnap
from scripts.iedb.drop_columns import drop_columns_antigens as drop_columns_antigens_iedb
from scripts.iedb.antigens_uniprot import antigens_uniprot
from scripts.iedb.drop_uniprot_columns import drop_uniprot_columns
from scripts.uniprot.drop_columns import drop_columns_antigen as uniprot_drop_columns

from scripts.antigens.join_files import join_files

def iedb_taskgroup(group_id):
    with TaskGroup(group_id=group_id) as taskgroup:

        start = EmptyOperator(task_id='start')

        drop_columns_antigens = PythonOperator(task_id='drop_columns_antigens', python_callable=drop_columns_antigens_iedb)

        download_antigens_uniprot = PythonOperator(task_id='download_antigens_uniprot', python_callable=antigens_uniprot)

        drop_columns_uniprot = PythonOperator(task_id='drop_columns_uniprot', python_callable=drop_uniprot_columns)

        end = EmptyOperator(task_id='end')

        start >> drop_columns_antigens >> download_antigens_uniprot >> drop_columns_uniprot >> end

    return taskgroup

default_args = {
    'owner': 'Kallox',
    'start_date': datetime(2022, 11, 3, 21, 0, 0)
}

with DAG(dag_id='get_antigens', default_args=default_args, schedule='@monthly') as dag:
    
    start = EmptyOperator(task_id='start')

    catnap = PythonOperator(task_id='catnap', python_callable=extract_catnap)

    iedb = iedb_taskgroup('iedb')

    uniprot = PythonOperator(task_id = 'uniprot', python_callable=uniprot_drop_columns)

    join_antigens = PythonOperator(task_id = 'join_antigens', python_callable=join_files)

    load_to_database = EmptyOperator(task_id='load_to_database')

    end = EmptyOperator(task_id='end')

    start >> catnap >> iedb >> uniprot >> join_antigens >> load_to_database >> end
