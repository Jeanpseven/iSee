import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import youtube_dl

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
        print(f"Arquivo baixado: {os.path.basename(urlparse(url).path)}")
    else:
        print(f"Erro ao baixar arquivo: {url}")

# Função para baixar um vídeo
def baixar_video(url, diretorio_destino):
    ydl_opts = {
        'outtmpl': os.path.join(diretorio_destino, '%(title)s.%(ext)s'),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Função para baixar todas as mídias do site
def baixar_midias_do_site(soup, url_site, diretorio_destino):
    midias = soup.find_all('img') + soup.find_all('video') + soup.find_all('audio')

    for midia in midias:
        url_midia = midia.get('src')
        if url_midia:
            url_absoluta = urljoin(url_site, url_midia)
            if tem_extensao_permitida(url_absoluta):
                if url_absoluta.endswith('.mp4'):
                    baixar_video(url_absoluta, diretorio_destino)
                else:
                    baixar_arquivo(url_absoluta, diretorio_destino)

# Obter o diretório padrão de downloads
diretorio_downloads = os.path.join(os.path.expanduser("~"), "Downloads")

# Solicitar a URL do site como input
url_site = input("Digite a URL do site: ")

# Diretório de destino para salvar as mídias
diretorio_destino = input(f"Digite o diretório de destino para salvar as mídias (padrão: {diretorio_downloads}): ")
if not diretorio_destino:
    diretorio_destino = diretorio_downloads

# Criar o diretório de destino, se não existir
os.makedirs(diretorio_destino, exist_ok=True)

# Fazer a requisição HTTP e obter o conteúdo HTML
response = requests.get(url_site)
html = response.content

# Criar o objeto Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

# Baixar todas as mídias do site
baixar_midias_do_site(soup, url_site, diretorio_destino)

# Exibir o caminho onde as mídias foram salvas
print(f"Mídias salvas em: {diretorio_destino}")
