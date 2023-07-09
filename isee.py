import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re

# Função para verificar se um elemento tem o estilo de desfoque
def tem_desfoque(elemento):
    estilo = elemento.get('style')
    if estilo:
        padrao_desfoque = r"(?:blur|opacity|filter|backdrop-filter):\s*(?:.+?);"
        if re.search(padrao_desfoque, estilo, flags=re.IGNORECASE):
            return True
    return False

# Função para remover elementos com desfoque
def remover_elementos_com_desfoque(soup):
    elementos_desfocados = soup.find_all(tem_desfoque)
    for elemento in elementos_desfocados:
        elemento.decompose()

# Função para remover diálogos de login ou cadastro
def remover_dialogos_login_cadastro(soup):
    dialogos = soup.find_all('dialog')
    for dialogo in dialogos:
        dialogo.decompose()

# Função para baixar todas as mídias do site
def baixar_midias_do_site(soup, url_site, diretorio_destino):
    midias = soup.find_all('img') + soup.find_all('video') + soup.find_all('audio')

    for midia in midias:
        url_midia = midia.get('src')
        if url_midia:
            url_absoluta = urljoin(url_site, url_midia)
            baixar_midia(url_absoluta, diretorio_destino)

# Função para fazer o download de uma mídia
def baixar_midia(url, diretorio):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        nome_arquivo = os.path.join(diretorio, os.path.basename(urlparse(url).path))
        with open(nome_arquivo, 'wb') as arquivo:
            for chunk in response.iter_content(1024):
                arquivo.write(chunk)
        print(f"Mídia baixada: {nome_arquivo}")
    else:
        print(f"Erro ao baixar mídia: {url}")

# URL do site
url_site = input("Digite a URL do site: ")

# Diretório de destino para salvar as mídias
diretorio_destino = input("Digite o diretório de destino para salvar as mídias: ")
os.makedirs(diretorio_destino, exist_ok=True)

# Fazer a requisição HTTP e obter o conteúdo HTML
response = requests.get(url_site)
html = response.content

# Criar o objeto Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

# Menu de opções
while True:
    print("\n[Menu de Opções]")
    print("1. Baixar Mídias")
    print("2. Remover Diálogos de Login ou Cadastro")
    print("3. Remover Blur")
    print("4. Executar Todas as Opções")
    print("0. Sair")

    opcao = input("\nDigite o número da opção desejada: ")

    if opcao == "1":
        baixar_midias_do_site(soup, url_site, diretorio_destino)
    elif opcao == "2":
        remover_dialogos_login_cadastro(soup)
    elif opcao == "3":
        remover_elementos_com_desfoque(soup)
    elif opcao == "4":
        baixar_midias_do_site(soup, url_site, diretorio_destino)
        remover_dialogos_login_cadastro(soup)
        remover_elementos_com_desfoque(soup)
    elif opcao == "0":
        break
    else:
        print("Opção inválida. Tente novamente.")

# Exibir o HTML resultante
print(soup.prettify())
