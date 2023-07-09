const axios = require('axios');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
const { promisify } = require('util');

// Função para baixar um arquivo
async function baixarArquivo(url, destino) {
  try {
    const response = await axios.get(url, { responseType: 'stream' });
    const caminhoArquivo = path.join(destino, path.basename(url));
    const writer = fs.createWriteStream(caminhoArquivo);
    response.data.pipe(writer);
    await promisify(writer.on).call(writer, 'finish');
    console.log(`Arquivo baixado: ${caminhoArquivo}`);
  } catch (error) {
    console.error(`Erro ao baixar arquivo: ${url}`);
    console.error(error.message);
  }
}

// Função para baixar um vídeo
async function baixarVideo(url, destino) {
  try {
    const caminhoDestino = path.join(destino, 'videos');
    if (!fs.existsSync(caminhoDestino)) {
      fs.mkdirSync(caminhoDestino, { recursive: true });
    }
    const output = path.join(caminhoDestino, '%(title)s.%(ext)s');
    const { exec } = require('child_process');
    const comando = `youtube-dl -o "${output}" ${url}`;
    await promisify(exec)(comando);
    console.log(`Vídeo baixado: ${url}`);
  } catch (error) {
    console.error(`Erro ao baixar vídeo: ${url}`);
    console.error(error.message);
  }
}

// Função para baixar todas as mídias do site
async function baixarMidiasDoSite(urlSite, destino) {
  try {
    const response = await axios.get(urlSite);
    const dom = new JSDOM(response.data);
    const document = dom.window.document;
    const midias = [...document.querySelectorAll('img, video')];
    
    for (const midia of midias) {
      let urlMidia;
      if (midia.tagName === 'IMG') {
        urlMidia = midia.src;
      } else if (midia.tagName === 'VIDEO') {
        urlMidia = midia.currentSrc;
      }
      
      if (urlMidia) {
        const extensao = path.extname(urlMidia).slice(1).toLowerCase();
        const urlAbsoluta = new URL(urlMidia, urlSite).href;
        
        if (['mp4', 'mov', 'mp3', 'img', 'jpg', 'jpeg', 'png', 'pdf', 'doc', 'avi', 'mkv', 'mpeg', 'vid'].includes(extensao)) {
          if (extensao === 'mp4') {
            await baixarVideo(urlAbsoluta, destino);
          } else {
            await baixarArquivo(urlAbsoluta, destino);
          }
        }
      }
    }
  } catch (error) {
    console.error(`Erro ao baixar mídias do site: ${urlSite}`);
    console.error(error.message);
  }
}

// Solicitar a URL do site
const readline = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
});

readline.question('Digite a URL do site: ', async (urlSite) => {
  // Diretório de destino para salvar as mídias
  const destino = path.join(process.env.HOME || process.env.USERPROFILE, 'Downloads');

  // Criar o diretório de destino, se não existir
  if (!fs.existsSync(destino)) {
    fs.mkdirSync(destino, { recursive: true });
  }

  // Baixar todas as mídias do site
  await baixarMidiasDoSite(urlSite, destino);

  // Exibir o caminho onde as mídias foram salvas
  console.log(`Mídias salvas em: ${destino}`);

  readline.close();
});
