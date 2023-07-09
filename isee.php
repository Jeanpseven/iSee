<?php

// Função para baixar um arquivo
function baixar_arquivo($url, $destino) {
    $conteudo = file_get_contents($url);
    file_put_contents($destino, $conteudo);
    echo "Arquivo baixado: " . basename($destino) . "\n";
}

// Função para baixar um vídeo
function baixar_video($url, $destino) {
    exec("youtube-dl -o \"$destino/%(title)s.%(ext)s\" \"$url\"");
}

// Função para baixar todas as mídias do site
function baixar_midias_do_site($url_site, $destino) {
    $html = file_get_contents($url_site);
    $midias = [];
    preg_match_all('/<img[^>]+>/', $html, $midias);
    preg_match_all('/<video[^>]+>/', $html, $midias_temp);
    $midias = array_merge($midias[0], $midias_temp[0]);

    foreach ($midias as $midia) {
        preg_match('/src="([^"]+)"/', $midia, $matches);
        if (isset($matches[1])) {
            $url_midia = $matches[1];
            $url_absoluta = rtrim($url_site, '/') . '/' . ltrim($url_midia, '/');
            $extensao = pathinfo($url_absoluta, PATHINFO_EXTENSION);
            if (preg_match('/^(mp4|mov|mp3|img|jpg|jpeg|png|pdf|doc|avi|mkv|mpeg|vid)$/', $extensao)) {
                if ($extensao == 'mp4') {
                    baixar_video($url_absoluta, $destino);
                } else {
                    baixar_arquivo($url_absoluta, $destino . '/' . basename($url_absoluta));
                }
            }
        }
    }
}

// Solicitar a URL do site
$url_site = readline("Digite a URL do site: ");

// Diretório de destino para salvar as mídias
$destino = readline("Digite o diretório de destino para salvar as mídias (padrão: Downloads): ");
$destino = $destino ?: 'Downloads';

// Criar o diretório de destino, se não existir
if (!file_exists($destino)) {
    mkdir($destino, 0777, true);
}

// Baixar todas as mídias do site
baixar_midias_do_site($url_site, $destino);

// Exibir o caminho onde as mídias foram salvas
echo "Mídias salvas em: " . realpath($destino) . "\n";
