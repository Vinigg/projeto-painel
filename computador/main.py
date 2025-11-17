import os
import serial
import threading
import time

from reconhecer_fala import capturar_e_detectar_lingua, get_whisper_model

porta = "COM6"  # Ajuste conforme necessário
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
        try:
            linha = ser.readline().decode(errors="ignore").strip()
        except Exception as e:
            print(f"Erro lendo da serial: {e}")
            time.sleep(0.5)
            continue

        if not linha:
            continue

        print("Recebido:", linha)

        if linha.lower() == "evento":
            print("Evento recebido: iniciando reconhecimento de fala.")
            iniciar_reconhecimento_assincrono()

if __name__ == "__main__":
    try:
        loop_serial()
    except KeyboardInterrupt:
        print("Encerrando...")
    finally:
        try:
            ser.close()
        except Exception:
            pass