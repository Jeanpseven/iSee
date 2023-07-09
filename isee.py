import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Função para verificar se uma URL possui uma das extensões permitidas
def tem_extensao_permitida(url):
    extensoes_permitidas = ['.mp4', '.mov', '.mp3', '.img', '.jpg', '.jpeg', '.png', '.pdf', '.doc', '.avi', '.mkv', '.mpeg', '.vid']
    return any(url.endswith(extensao) for extensao in extensoes_permitidas)

# Função para baixar um arquivo
def baixar_arquivo(url, diretorio_destino):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        nome_arquivo = os.path.join(diretorio_destino, os.path.basename(urlparse(url).path))
        with open(nome_arquivo, 'wb') as arquivo:
            for chunk in response.iter_content(1024):
                arquivo.write(chunk)
        print(f"Arquivo baixado: {nome_arquivo}")
    else:
        print(f"Erro ao baixar arquivo: {url}")

# Função para baixar todos os arquivos permitidos do site
def baixar_arquivos_do_site(soup, url_site, diretorio_destino):
    links = soup.find_all('a', href=True)
    for link in links:
        url_link = link.get('href')
        if url_link and tem_extensao_permitida(url_link):
            url_absoluta = urljoin(url_site, url_link)
            baixar_arquivo(url_absoluta, diretorio_destino)

# Obter o diretório padrão de downloads
diretorio_downloads = os.path.join(os.path.expanduser("~"), "Downloads")

# Solicitar a URL do site como input
url_site = input("Digite a URL do site: ")

# Diretório de destino para salvar os arquivos
diretorio_destino = input(f"Digite o diretório de destino para salvar os arquivos (padrão: {diretorio_downloads}): ")
if not diretorio_destino:
    diretorio_destino = diretorio_downloads

# Criar o diretório de destino, se não existir
os.makedirs(diretorio_destino, exist_ok=True)

# Fazer a requisição HTTP e obter o conteúdo HTML
response = requests.get(url_site)
html = response.content

# Criar o objeto Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

# Baixar todos os arquivos permitidos do site
baixar_arquivos_do_site(soup, url_site, diretorio_destino)

# Exibir o caminho onde os arquivos foram salvos
print(f"Arquivos salvos em: {diretorio_destino}")
