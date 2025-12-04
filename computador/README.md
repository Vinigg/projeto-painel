# Painel Inteligente: Detecção de Idioma + Propaganda

Sistema que, ao receber um evento pela porta serial (Arduino), grava áudio por alguns segundos, detecta o idioma com Whisper e exibe automaticamente uma propaganda correspondente em tela usando Pygame. Quando não há exibição ativa, mostra sempre a imagem default.

## Visão Geral
- Evento serial aciona a captura de áudio (PyAudio) e salva em `temp/ultima_captura.wav`.
- Whisper (openai-whisper) detecta o idioma do áudio gravado.
- `controlar_exibicao.py` exibe a imagem associada ao idioma em tela (Pygame).
- Após o tempo configurado, volta para a imagem `default.jpeg`.

## Recursos
- Detecção de idioma com Whisper.
- Exibição gráfica em Pygame com overlay informativo.
- Imagem default exibida na inicialização e entre propagandas.
- Estatísticas de exibição salvas em `estatisticas_exibicao.json`.

## Requisitos
- Windows 10/11
- Python 3.11 (recomendado; evita problemas de compatibilidade com PyAudio)
- Placa Arduino (opcional, para acionar o evento serial)

## Preparação do Ambiente (Windows PowerShell)

1) Verifique versões instaladas de Python:
```powershell
py -0p
```

2) Crie uma venv com Python 3.11 (se você tiver 3.11 instalado):
```powershell
py -3.11 -m venv .\computador\venv311
```

Se não aparecer Python 3.11 em `py -0p`, instale o Python 3.11 pelo site oficial e repita o comando acima.

3) Ative a venv:
```powershell
.\computador\venv311\Scripts\Activate.ps1
```

4) Atualize `pip` e instale dependências:
```powershell
python -m pip install --upgrade pip
pip install -r .\computador\requirements.txt
```

Dependências principais: `pyserial`, `PyAudio`, `numpy`, `openai-whisper`, `pygame`.

## Estrutura de Pastas
```
projeto-painel/
  computador/
    main.py
    reconhecer_fala.py
    controlar_exibicao.py
    config_exibicao.json
    requirements.txt
    images/            <- coloque aqui as imagens
      default.jpeg
      pt.jpg | en.jpg | es.jpg | fr.jpg | de.jpg | it.jpg
    temp/
```

## Configuração
- `config_exibicao.json` controla tamanho de tela, tempo de exibição, pasta de imagens (`images`), e overlay.
- O sistema tenta carregar propagandas por ordem: `lingua.jpg` → `lingua.png` → nomes mapeados (portugues.jpg, ingles.jpg, ...) → `default`.
- A imagem `default.jpeg` deve existir em `computador/images/`.

## Execução
1) Ative a venv (se ainda não estiver ativa):
```powershell
.\computador\venv311\Scripts\Activate.ps1
```

2) Entre na pasta `computador` e rode:
```powershell
cd .\computador
python .\main.py
```

3) Fluxo de funcionamento:
- O programa fica escutando a porta serial (ex.: `COM6`, 9600 baud).
- Ao receber o texto `evento`, grava áudio por ~10s e detecta o idioma.
- Exibe a propaganda do idioma detectado por `tempo_exibicao` (padrão 30s) e volta para `default.jpeg`.

## Ajustes Importantes
- Porta serial: ajuste em `main.py` a porta (`COMx`) conforme seu Arduino.
- Imagens: coloque os arquivos `pt.jpg`, `en.jpg`, `es.jpg`, `fr.jpg`, `de.jpg`, `it.jpg` e `default.jpeg` na pasta `images/`.
- Performance: modelos Whisper maiores são mais precisos e mais lentos. O padrão é leve para Windows.

## Controles de Teclado (Janela Pygame)
- `ESC`: encerra a exibição atual e volta para `default.jpeg`
- `Q`: encerra o programa
- `SPACE`: pula a exibição atual e volta para `default.jpeg`

## Solução de Problemas
- PyAudio falha para Python mais recente: use Python 3.11 e a venv acima.
- Whisper pede ffmpeg: nossa implementação carrega `wav` direto, sem ffmpeg.
- Imagem não aparece: verifique `config_exibicao.json` → `pasta_imagens` deve ser `images` e os nomes de arquivo corretos.
## Licença
Projeto educacional. Imagens de propaganda são fornecidas pelo usuário.
