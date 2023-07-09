#!/bin/bash

# Função para baixar um arquivo
function baixar_arquivo() {
    url="$1"
    destino="$2"
    curl -L -o "$destino" "$url"
    echo "Arquivo baixado: $(basename "$destino")"
}

# Função para baixar um vídeo
function baixar_video() {
    url="$1"
    destino="$2"
    youtube-dl -o "$destino/%(title)s.%(ext)s" "$url"
}

# Função para baixar todas as mídias do site
function baixar_midias_do_site() {
    url_site="$1"
    destino="$2"

    html=$(curl -s "$url_site")
    midias=$(echo "$html" | grep -Eo '<img src="[^"]+"|<video[^>]+>')
    
    for midia in $midias; do
        url_midia=$(echo "$midia" | grep -Eo 'src="[^"]+"' | cut -d '"' -f 2)
        if [ -n "$url_midia" ]; then
            url_absoluta="$url_site/$url_midia"
            extensao="${url_absoluta##*.}"
            if [[ "$extensao" =~ ^(mp4|mov|mp3|img|jpg|jpeg|png|pdf|doc|avi|mkv|mpeg|vid)$ ]]; then
                if [[ "$extensao" == "mp4" ]]; then
                    baixar_video "$url_absoluta" "$destino"
                else
                    baixar_arquivo "$url_absoluta" "$destino"
                fi
            fi
        fi
    done
}

# Solicitar a URL do site
read -p "Digite a URL do site: " url_site

# Diretório de destino para salvar as mídias
read -p "Digite o diretório de destino para salvar as mídias (padrão: Downloads): " destino
destino="${destino:-Downloads}"

# Criar o diretório de destino, se não existir
mkdir -p "$destino"

# Baixar todas as mídias do site
baixar_midias_do_site "$url_site" "$destino"

# Exibir o caminho onde as mídias foram salvas
echo "Mídias salvas em: $(realpath "$destino")"
