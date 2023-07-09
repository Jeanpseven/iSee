import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Função para verificar se uma URL possui uma das extensões permitidas
def tem_extensao_permitida(url):
    extensoes_permitidas = ['.mp4', '.mov', '.mp3', '.img', '.jpg', '.jpeg', '.png', '.pdf', '.doc']
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

# Solicitar a URL do site como input
url_site = input("Digite a URL do site: ")

# Criar o diretório de destino para salvar os arquivos
diretorio_destino = input("Digite o diretório de destino para salvar os arquivos: ")
os.makedirs(diretorio_destino, exist_ok=True)

# Fazer a requisição HTTP e obter o conteúdo HTML
response = requests.get(url_site)
html = response.content

# Criar o objeto Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

# Baixar todos os arquivos permitidos do site
baixar_arquivos_do_site(soup, url_site, diretorio_destino)
