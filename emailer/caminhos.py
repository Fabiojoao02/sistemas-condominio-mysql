from pathlib import Path
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# caminho = r'c:\\user\\fabio\\desktop\\exemplo'
# home do meu usuario

# load_dotenv()
host = "smtp.gmail.com"
port = 587
login = 'condodaspalmeiras50@gmail.com'
senha = 'zsgzaefsocmdtgrm'

server = smtplib.SMTP(host, port)
server.ehlo()
server.starttls()
server.login(login, senha)

'''
print(Path.home())

CAMINHO_ARQUIVO = Path(__file__).parent
mesano = '022023'
# caminho = os.path.join(CAMINHO_ARQUIVO, 'templates\emailer', mesano)
# arquivo = '301'+'.PDF'
caminho = CAMINHO_ARQUIVO / 'templates\emailer' / mesano
# caminho.touch
# caminho.unlink  # apagar
caminho.mkdir(exist_ok=True)
caminho = CAMINHO_ARQUIVO / 'templates\emailer' / mesano  # / arquivo
print(caminho)

# print(CAMINHO_ARQUIVO)
# diretorio, arquivo = os.path.split(caminho)
# print(caminho)
# print(CAMINHO_ARQUIVO)
# print(os.path.exists(caminho))
# if not os.path.exists(caminho):
#    print('Caminho nao existe, entao vou criar')
'''
