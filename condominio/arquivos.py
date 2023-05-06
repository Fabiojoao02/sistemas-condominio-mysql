from pathlib import Path

caminho_arquivo = Path(__file__).parent.parent
arquivo = caminho_arquivo / 'emailer' / 'templates' / \
    'emailer' / '022023' / 'arquivo.txt'
# 'relatoriocalculospdf.pdf'
# arquivo = '\\WorkSpacesCondominio\\imailer\\templates\\emailer\\022023\\arquivo.txt'

# FileNotFoundError: [Errno 2] No such file or directory: 'f:\\WorkSpacesCondominio\\imailer\\templates\\emailer\\022023\\arquivo.txt'
print(arquivo)
arquivo.touch()  # cria
print(arquivo)
arquivo.unlink()  # exclui
