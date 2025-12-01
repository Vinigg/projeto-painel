import os
import serial
import threading
import time

from reconhecer_fala import capturar_e_detectar_lingua, get_whisper_model
from controlar_exibicao import ControladorExibicao

# Inicializar controlador de exibição
controlador_exibicao = ControladorExibicao()

porta = "COM7"  # Ajuste conforme necessário
baud = 9600

# Toggle para decidir se carrega modelo Whisper antes de escutar (reduz latência do primeiro evento)
PRELOAD_MODELO = os.getenv("PRELOAD_MODELO", "1") == "1"

ser = serial.Serial(porta, baud, timeout=1)
ser.reset_input_buffer()

if PRELOAD_MODELO:
    print("Carregando modelo Whisper antes de iniciar loop serial...")
    _ = get_whisper_model()  # força carregamento
    print("Modelo carregado. Aguardando evento da porta serial...")
else:
    print("Aguardando evento da porta serial (modelo será carregado na 1ª captura)...")

# Flag para evitar múltiplos reconhecimentos simultâneos
_reconhecimento_em_andamento = False

def _thread_reconhecimento():
    global _reconhecimento_em_andamento
    try:
        print("Iniciando captura e detecção de língua (≈10s)...")
        # Usa valores padrão configurados em reconhecer_fala.py (10s, 16kHz)
        lingua, confianca = capturar_e_detectar_lingua()
        if lingua:
            print(f"Língua detectada: {lingua} (confiança ~{confianca})")
            
            # Exibir propaganda no controlador de exibição
            sucesso = controlador_exibicao.exibir_imagem_lingua(lingua)
            if sucesso:
                print(f"✅ Propaganda iniciada para idioma: {lingua}")
            else:
                print(f"⚠️ Não foi possível iniciar propaganda para: {lingua}")
            
            # Enviar resultado pela serial
            try:
                ser.write(f"lingua:{lingua}\n".encode())
            except Exception as e:
                print(f"Falha ao enviar resultado pela serial: {e}")
        else:
            print("Não foi possível detectar a língua no áudio.")
    except Exception as e:
        print(f"Erro durante reconhecimento: {e}")
    finally:
        _reconhecimento_em_andamento = False

def iniciar_reconhecimento_assincrono():
    global _reconhecimento_em_andamento
    if _reconhecimento_em_andamento:
        print("Reconhecimento já em andamento. Ignorando novo evento.")
        return
    _reconhecimento_em_andamento = True
    t = threading.Thread(target=_thread_reconhecimento, daemon=True)
    t.start()

def loop_serial():
    while True:
        # Processar eventos do Pygame (importante para manter tela responsiva)
        if not controlador_exibicao.processar_eventos():
            print("👋 Encerrando aplicação...")
            break
        
        # Verificar se tempo de exibição expirou
        controlador_exibicao.verificar_tempo_exibicao()
        
        try:
            linha = ser.readline().decode(errors="ignore").strip()
        except Exception as e:
            print(f"Erro lendo da serial: {e}")
            time.sleep(0.1)
            continue

        if linha:
            print("Recebido:", linha)

            if linha.lower() == "evento":
                print("Evento recebido: iniciando reconhecimento de fala.")
                iniciar_reconhecimento_assincrono()
        
        # Pequeno delay para não sobrecarregar CPU
        time.sleep(0.05)

if __name__ == "__main__":
    print("🎬 Sistema de painel inteligente iniciado")
    print("Controles: ESC - Encerrar exibição | Q - Sair | ESPAÇO - Pular propaganda")
    
    try:
        loop_serial()
    except KeyboardInterrupt:
        print("\n⌨️ Ctrl+C detectado. Encerrando...")
    finally:
        print("🧹 Limpando recursos...")
        try:
            ser.close()
        except Exception:
            pass
        controlador_exibicao.encerrar()
        print("👋 Sistema encerrado com sucesso!")