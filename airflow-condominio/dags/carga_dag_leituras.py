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
import shutil
from pathlib import Path
import mysql.connector

# from django.db import connection
# import django

# Configurações para o Django
# Substitua 'seu_projeto' pelo nome do seu projeto Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistemacondominio.settings')
# django.setup()


# Configurar as informações de conexão
mysql_config = {
    'database': 'condominio',
    'user': 'root',
    'password': '',
    #    'host': '127.0.0.1'
    'host': 'host.docker.internal'

}

# 'user': 'vacom_fabiojoao',
# 'password': 'D&lteco2023',
# 'host': '108.167.132.104',
# 'database': 'vacom_condominio'

default_args = {
    'depends_on_past': False,
    'email': ['fbianastacio@gmail.com'],
    'email_on_failure': True,  # True
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}

# schedule_interval="*/3 * * * * "
dag = DAG('carga_leitura', description='Dados da Leitura',
          schedule_interval=None, start_date=datetime(2023, 9, 10),

          catchup=False, default_args=default_args, default_view='graph',
          doc_md="## Dag para registrar as leituras do Mês e Ano")

group_check_temp = TaskGroup("group_check_temp", dag=dag)
group_database = TaskGroup('group_database', dag=dag)


file_sensor_task = FileSensor(
    task_id='file_sensor_task',
    filepath=Variable.get('path_file_lei'),
    fs_conn_id='fs_default_lei',
    poke_interval=10,
    dag=dag)


def process_file(**kwarg):
    # df_gas = pd.read_excel(Variable.get('path_file'), sheet_name='gas')
    df_mov = pd.read_csv(Variable.get('path_file_lei'), delimiter=';',
                         encoding='utf-8')

    # condominio = df_mov['condominio']
    mesano = df_mov['mesano'] = df_mov['mesano'].apply(
        lambda x: str(x).zfill(6)).tolist()
    bloco = df_mov['bloco'].tolist()
    #
    kwarg['ti'].xcom_push(key='bloco', value=bloco)
    kwarg['ti'].xcom_push(key='mesano', value=mesano)
    kwarg['ti'].xcom_push(key='conta', value=df_mov['conta'].tolist())
    kwarg['ti'].xcom_push(
        key='id_morador', value=df_mov['id_morador'].tolist())
    kwarg['ti'].xcom_push(key='leitura_inicial',
                          value=df_mov['leitura_inicial'].tolist())
    kwarg['ti'].xcom_push(key='leitura_final',
                          value=df_mov['leitura_final'].tolist())
    kwarg['ti'].xcom_push(
        key='dt_leitura', value=df_mov['dt_leitura'].tolist())

    kwarg['ti'].xcom_push(
        key='valorM3', value=df_mov['valorM3'].tolist())

    if mesano:
        email_ok = 1
    else:
        email_ok = 0

    # Copia o arquivo
    shutil.copy(Variable.get('path_file_lei'),
                Variable.get('path_file_exp_lei'))
    # remova arquivo da pasta
    os.remove(Variable.get('path_file_lei'))

    return email_ok


# NotADirectoryError: [Errno 20] Not a directory: '/opt/airflow/data/cargas.xlsx'
get_data = PythonOperator(
    task_id='get_data',
    python_callable=process_file,
    provide_context=True,
    dag=dag)


def insert_data(ti):
    # Crie uma conexão com o banco de dados MySQL

    conn = mysql.connector.connect(**mysql_config)
    blocos = ti.xcom_pull(task_ids="get_data", key="bloco")
    mesanos = ti.xcom_pull(task_ids="get_data", key="mesano")
    contas = ti.xcom_pull(task_ids="get_data", key="conta")
    id_moradores = ti.xcom_pull(task_ids="get_data", key="id_morador")
    leitura_inicials = ti.xcom_pull(task_ids="get_data", key="leitura_inicial")
    leitura_finals = ti.xcom_pull(task_ids="get_data", key="leitura_final")
    dt_leituras = ti.xcom_pull(task_ids="get_data", key="dt_leitura")
    valorm3s = ti.xcom_pull(task_ids="get_data", key="valorM3")

    cursor = conn.cursor()
    with conn.cursor() as cursor:

        for bloco, mesano, conta, id_morador, leitura_inicial, leitura_final, dt_leitura, valorm3 in zip(blocos, mesanos, contas, id_moradores, leitura_inicials, leitura_finals, dt_leituras, valorm3s):

            cursor.execute('''INSERT INTO leituras (id_bloco, mesano, id_contas, id_morador,leitura_inicial,leitura_final, dt_leitura, valor_m3)
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s);''',
                           (bloco, mesano, conta, id_morador, float(leitura_inicial.replace(',', '.')), float(leitura_final.replace(',', '.')), datetime.strptime(dt_leitura, '%d/%m/%Y').date(),  float(valorm3.replace(',', '.'))
                            )
                           )
        conn.commit()
# datetime.strptime(dt_leitura, '%d/%m/%Y').date().strftime('%Y/%m/%d'),


def delete_data(ti):
    # Crie uma conexão com o banco de dados MySQL

    conn = mysql.connector.connect(**mysql_config)

    blocos = ti.xcom_pull(task_ids="get_data", key="bloco")
    mesanos = ti.xcom_pull(task_ids="get_data", key="mesano")

    print(blocos)
    print(mesanos)

    cursor = conn.cursor()
    with conn.cursor() as cursor:
        for bloco, mesano in zip(blocos, mesanos):
            cursor.execute(
                '''DELETE FROM leituras where id_bloco=%s and mesano=%s;''', (bloco, mesano))
        conn.commit()


insert_data_task = PythonOperator(
    task_id='insert_data',
    python_callable=insert_data,
    task_group=group_database,
    dag=dag
)

delete_data_task = PythonOperator(
    task_id='delete_data',
    python_callable=delete_data,
    task_group=group_database,
    dag=dag
)


send_email_alert = EmailOperator(
    task_id='send_email_alert',
    to='fbianastacio@gmail.com',
    subject='Airlfow alert',
    html_content='''<h3>Alerta de Temperatrura Leituras. </h3>
                                <p> Dag: carga_leitura </p>
                                ''',
    task_group=group_check_temp,
    dag=dag)

send_email_normal = EmailOperator(
    task_id='send_email_normal',
    to='fbianastacio@gmail.com',
    subject='Airlfow advise',
    html_content='''<h3>Temperaturas Leituras normais . </h3>
                                <p> Dag: carga_leitura </p>
                                ''',
    task_group=group_check_temp,
    dag=dag)


def avalia_temp(ti):
    number = ti.xcom_pull(task_ids='get_data')
    print(number)
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
    delete_data_task >> insert_data_task


file_sensor_task >> get_data
get_data >> group_check_temp
# get_data >> insert_data_task
get_data >> group_database
