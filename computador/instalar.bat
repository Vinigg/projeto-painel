@echo off
echo Instalando dependências do Painel Inteligente...
pip install pyserial SpeechRecognition pygame langdetect pyaudio
echo.
echo Criando estrutura de pastas...
mkdir imagens
echo.
echo ✅ Instalação concluída!
echo.
echo Coloque suas imagens na pasta 'imagens' com os nomes:
echo pt.jpg, en.jpg, es.jpg, fr.jpg, de.jpg, default.jpg
pause