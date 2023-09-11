from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.http.sensors.http import HttpSensor
import requests
import pandas as pd
import os
import shutil
from pathlib import Path
from airflow.utils.email import send_email
from django.db import connection
import django
# from . models import  Leituras, Calculos, Bloco

# Configurações para o Django
# Substitua 'seu_projeto' pelo nome do seu projeto Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistemacondominio.settings')
django.setup()


ROOT_FOLDER = Path(__file__).parent
CAMINHO_ARQUIVO = ROOT_FOLDER / 'arquivos_carga' / 'cargas.xlsx'

print(CAMINHO_ARQUIVO)


df_gas = pd.read_excel(CAMINHO_ARQUIVO, sheet_name='gas')

df_mov = pd.read_excel(CAMINHO_ARQUIVO, sheet_name='movimento')


# Controle "DELTA" para Insert dos dados
# Percorrer as linhas do arquivo Excel e executar a consulta SQL com os valores correspondentes
# delete

condominio = df_mov['condominio']
mesano = df_mov['mesano'] = df_mov['mesano'].apply(lambda x: str(x).zfill(6))
bloco = df_mov['bloco']

# Movimentação
# Delete se encontrar movimento
with connection.cursor() as cursor:
    for m, b in zip(mesano, bloco):
        cursor.execute('''
        DELETE FROM movimento WHERE mesano=%s AND id_bloco=%s AND situacao = 'A'
        ''', (m, b))
        # connection.commit()

# inseri dados na movimento
for index, row in df_mov.iterrows():

    # Executa a consulta SQL bruta e itera sobre os resultados
    with connection.cursor() as cursor:
        cursor.execute('''
            insert into movimento  (mesano,id_bloco,id_contas,id_tipo_calculo,valor) values (%s,%s,%s,%s,%s)
            ''', [(str(row['mesano']).zfill(6)), row['bloco'],  row['conta'], row['tipoCalculo'], row['valor']]
        )


# Leitura do Gas


condominio = df_gas['condominio']
mesano = df_gas['mesano'] = df_gas['mesano'].apply(lambda x: str(x).zfill(6))
bloco = df_gas['bloco']

# Delete se encontrar movimento
with connection.cursor() as cursor:
    for m, b in zip(mesano, bloco):
        cursor.execute('''
        DELETE FROM leituras WHERE mesano=%s AND id_bloco=%s 
        ''', (m, b))
        # connection.commit()

# inseri dados na movimento
for index, row in df_gas.iterrows():

    # Verificar se o registro já existe na tabela
    val_check = (
        (str(row['mesano']).zfill(
            6)), row['bloco'],  row['id_morador'],  row['conta'], row['dt_leitura'], row['leitura_inicial'], row['leitura_final'], row['valorM3']
    )
    print(val_check)

    # Executa a consulta SQL bruta e itera sobre os resultados
    with connection.cursor() as cursor:
        cursor.execute('''
          insert into leituras  (mesano,id_bloco,id_morador,id_contas,dt_leitura,leitura_inicial, leitura_final,valor_M3) values (%s,%s,%s,%s,%s,%s,%s,%s)
         ''', [(str(row['mesano']).zfill(6)), row['bloco'],  row['id_morador'],  row['conta'], row['dt_leitura'], row['leitura_inicial'], row['leitura_final'], row['valorM3']]
        )
