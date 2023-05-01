from pathlib import Path
import shutil

# caminho = r'c:\\user\\fabio\\desktop\\exemplo'
# home do meu usuario
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
