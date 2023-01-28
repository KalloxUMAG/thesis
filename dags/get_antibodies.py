from datetime import datetime

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from scripts.catnap.extract import extract as extract_catnap
from scripts.covabdab.extract import extract as extract_covabdab
from scripts.uniprot.drop_columns import drop_columns_antibody as uniprot_drop_columns
from scripts.vdjdb.extract_antibodies import extract_antibodies as extract_vdjdb

from scripts.antibodies.join_files import join_files


default_args = {
    'owner': 'Kallox',
    'start_date': datetime(2022, 11, 3, 21, 0, 0)
}

with DAG(dag_id='get_antibodies', default_args=default_args, schedule='@monthly') as dag:
    
    start = EmptyOperator(task_id='start')

    catnap = PythonOperator(task_id='catnap', python_callable=extract_catnap)

    covabdab = PythonOperator(task_id='covabdab', python_callable=extract_covabdab)

    imgt = EmptyOperator(task_id='imgt')

    uniprot = PythonOperator(task_id = 'uniprot', python_callable=uniprot_drop_columns)

    vdjdb = PythonOperator(task_id = 'vdjdb', python_callable=extract_vdjdb)

    join_antibodies = PythonOperator(task_id = 'join_antibodies', python_callable=join_files)

    drop_exist_antibodies = EmptyOperator(task_id='drop_exists')

    properties = EmptyOperator(task_id='properties')

    load_to_database = EmptyOperator(task_id='load_to_database')

    end = EmptyOperator(task_id='end')

    start >> catnap >> covabdab >> imgt >> uniprot >> vdjdb >> join_antibodies >> load_to_database >> end

