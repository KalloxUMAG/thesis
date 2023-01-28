from datetime import datetime

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

from scripts.characterization.generate_fasta import csv_to_fasta
from scripts.characterization.gene_ontology import gene_ontology as go
from scripts.characterization.structural_characterization import structural_characterization
go
default_args = {
    'owner': 'Kallox',
    'start_date': datetime(2022, 10, 30, 20, 30, 0)
}

with DAG(dag_id='characterization', default_args=default_args, schedule='@once') as dag:
    start = EmptyOperator(task_id='start')

    generate_fasta = PythonOperator(task_id='generate_fasta', python_callable=csv_to_fasta)

    gene_ontology = PythonOperator(task_id='gene_ontology', python_callable=go)

    structural_prediction = PythonOperator(task_id='structural_prediction', python_callable=structural_characterization)

    physichochemical_properties = PythonOperator(task_id='physichochemical_properties', python_callable=)

    #pfam_prediction = PythonOperator(task_id='pfam_prediction', python_callable=)

    end = EmptyOperator(task_id='end')

    start >> generate_fasta >> gene_ontology >> structural_prediction >> physichochemical_properties >> end
