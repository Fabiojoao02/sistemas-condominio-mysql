# Domine Apache Airflow. https://www.eia.ai/
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.email import EmailOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.sensors.filesystem import FileSensor
from airflow.models import Variable
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
import pandas as pd
import os
# from django.db import connection
# import django

# Configurações para o Django
# Substitua 'seu_projeto' pelo nome do seu projeto Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistemacondominio.settings')
# django.setup()

default_args = {
    'depends_on_past': False,
    'email': ['fbianastacio@gmail.com'],
    'email_on_failure': False,  # True
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}

# schedule_interval="*/3 * * * * "
dag = DAG('windturbine', description='Dados da Turbina',
          schedule_interval=None, start_date=datetime(2023, 9, 10),
          catchup=False, default_args=default_args, default_view='graph',
          doc_md="## Dag para registrar os movimentos e as leituras do Mês e Ano")

group_check_temp = TaskGroup("group_check_temp", dag=dag)
group_database = TaskGroup('group_database', dag=dag)


file_sensor_task = FileSensor(
    task_id='file_sensor_task',
    filepath=Variable.get('path_file'),
    fs_conn_id='fs_default',
    poke_interval=10,
    dag=dag)


def process_file(**kwarg):
    # df_gas = pd.read_excel(Variable.get('path_file'), sheet_name='gas')
    df_mov = pd.read_excel(Variable.get('path_file'), sheet_name='movimento')
    #
    # condominio = df_mov['condominio']
    # mesano = df_mov['mesano'] = df_mov['mesano'].apply(
    #    lambda x: str(x).zfill(6))
    # bloco = df_mov['bloco']
    #
    # kwarg['ti'].xcom_push(key='bloco', value=bloco)
    # kwarg['ti'].xcom_push(key='mesano', value=mesano)
    # kwarg['ti'].xcom_push(key='conta', value=df_mov['conta'])
    # kwarg['ti'].xcom_push(key='tipoCalculo', value=df_mov['tipoCalculo'])
    # kwarg['ti'].xcom_push(key='valor', value=df_mov['valor'])

    kwarg['ti'].xcom_push(key='bloco', value='bloco')
    kwarg['ti'].xcom_push(key='mesano', value='mesano')
    kwarg['ti'].xcom_push(key='conta', value=['conta'])
    kwarg['ti'].xcom_push(key='tipoCalculo', value=['tipoCalculo'])
    kwarg['ti'].xcom_push(key='valor', value=['valor'])

   # os.remove(Variable.get('path_file'))
    # airflow-condominio\data\airflow
    # print('path_file')
    # os.listdir('/opt/airflow/data/')


# NotADirectoryError: [Errno 20] Not a directory: '/opt/airflow/data/cargas.xlsx'
get_data = PythonOperator(
    task_id='get_data',
    python_callable=process_file,
    provide_context=True,
    dag=dag)

create_table = PostgresOperator(task_id="create_table",
                                postgres_conn_id='postgres',
                                sql='''create table if not exists
                                movimento (bloco varchar, 
                                mesano varchar,
                                conta varchar,
                                tipoCalculo varchar,
                                valor varchar);
                                ''',
                                task_group=group_database,
                                dag=dag)

insert_data = PostgresOperator(task_id='insert_data',
                               postgres_conn_id='postgres',
                               parameters=(
                                   '{{ ti.xcom_pull(task_ids="get_data",key="bloco") }}',
                                   '{{ ti.xcom_pull(task_ids="get_data",key="mesano") }}',
                                   '{{ ti.xcom_pull(task_ids="get_data",key="conta") }}',
                                   '{{ ti.xcom_pull(task_ids="get_data",key="tipoCalculo") }}',
                                   '{{ ti.xcom_pull(task_ids="get_data",key="valor") }}'
                               ),
                               sql='''INSERT INTO sensors (bloco, mesano,
                               conta, tipoCalculo, valor)
                               VALUES (%s, %s, %s, %s, %s);''',
                               task_group=group_database,
                               dag=dag
                               )

send_email_alert = EmailOperator(
    task_id='send_email_alert',
    to='fbianastacio@gmail.com',
    subject='Airlfow alert',
    html_content='''<h3>Alerta de Temperatrura. </h3>
                                <p> Dag: windturbine </p>
                                ''',
    task_group=group_check_temp,
    dag=dag)

send_email_normal = EmailOperator(
    task_id='send_email_normal',
    to='fbianastacio@gmail.com',
    subject='Airlfow advise',
    html_content='''<h3>Temperaturas normais. </h3>
                                <p> Dag: windturbine </p>
                                ''',
    task_group=group_check_temp,
    dag=dag)


def avalia_temp(**context):
    number = float(context['ti'].xcom_pull(
        task_ids='get_data', key="encontrou_reg_mov"))
    if number == 0:
        return 'group_check_temp.send_email_alert'
    else:
        return 'group_check_temp.send_email_normal'


check_temp_branc = BranchPythonOperator(
    task_id='check_temp_branc',
    python_callable=avalia_temp,
    provide_context=True,
    dag=dag,
    task_group=group_check_temp)


with group_check_temp:
    check_temp_branc >> [send_email_alert, send_email_normal]

with group_database:
    create_table >> insert_data


file_sensor_task >> get_data
get_data >> group_check_temp
get_data >> group_database
