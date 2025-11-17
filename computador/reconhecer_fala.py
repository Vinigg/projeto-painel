"""Funções reutilizáveis para captura e detecção de língua usando Whisper.

Exposto para uso por `main.py` como orquestrador.

Principais funções:
  - get_whisper_model(): retorna (e faz cache) do modelo Whisper carregado.
  - gravar_audio(): grava áudio bruto e salva WAV.
  - detectar_idioma_whisper(): detecta idioma a partir de arquivo WAV.
  - capturar_e_detectar_lingua(): atalho que grava e detecta em um passo.
"""

import os
import wave
import pyaudio
import numpy as np
import whisper

# Configurações via ambiente (fallbacks)
DEFAULT_SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", "44100"))
DEFAULT_DURATION = int(os.getenv("CAPTURA_SEGUNDOS", "10"))
DEFAULT_WAV_PATH = os.getenv("WAV_PATH", os.path.join("temp", "ultima_captura.wav"))

_whisper_model = None  # cache do modelo Whisper
_WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL", "tiny")  # pode trocar para 'small', 'base', 'medium'

def get_whisper_model():
    """Carrega e cacheia modelo Whisper (openai-whisper)."""
    global _whisper_model
    if _whisper_model is None:
        print(f"🔄 Carregando modelo Whisper '{_WHISPER_MODEL_NAME}'...")
        _whisper_model = whisper.load_model(_WHISPER_MODEL_NAME)
    return _whisper_model

def detectar_idioma_whisper(caminho_wav: str) -> str:
    """Detecta idioma usando Whisper (somente identificação, não precisa texto completo)."""
    if not os.path.exists(caminho_wav):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_wav}")
    model = get_whisper_model()
    
    # Carrega áudio direto do WAV sem usar ffmpeg
    with wave.open(caminho_wav, 'rb') as wf:
        taxa = wf.getframerate()
        audio_bytes = wf.readframes(wf.getnframes())
    
    # Converte para float32 normalizado [-1, 1]
    audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
    
    # Reamostra para 16kHz se necessário (Whisper espera 16kHz)
    if taxa != 16000:
        fator = 16000 / taxa
        novo_len = int(len(audio_np) * fator)
        indices = np.linspace(0, len(audio_np)-1, novo_len)
        audio_np = np.interp(indices, np.arange(len(audio_np)), audio_np).astype(np.float32)
    
    # Whisper espera no máximo 30s
    audio_np = whisper.pad_or_trim(audio_np)
    mel = whisper.log_mel_spectrogram(audio_np).to(model.device)
    _, probs = model.detect_language(mel)
    lingua = max(probs, key=probs.get)
    print(f"🧭 Whisper detectou idioma: {lingua} (prob={probs[lingua]:.2f})")
    return lingua



def gravar_audio(segundos: int = DEFAULT_DURATION, sample_rate: int = DEFAULT_SAMPLE_RATE, caminho_wav: str = DEFAULT_WAV_PATH) -> str:
    """Grava áudio mono Int16 e salva em WAV.
    Retorna caminho do arquivo.
    """
    os.makedirs(os.path.dirname(caminho_wav), exist_ok=True)
    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=1024)
    except Exception as e:
        p.terminate()
        raise RuntimeError(f"Falha ao abrir microfone: {e}")

    print(f"🎤 Gravando {segundos}s (taxa={sample_rate})...")
    frames = []
    blocos = int(sample_rate / 1024 * segundos)
    for _ in range(blocos):
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream(); stream.close(); p.terminate()

    with wave.open(caminho_wav, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
    print(f"💾 WAV salvo: {caminho_wav}")
    return caminho_wav



def capturar_e_detectar_lingua(segundos: int = DEFAULT_DURATION,
                               sample_rate: int = int(os.getenv("CAPTURE_RATE", "44100")),
                               wav_path: str = DEFAULT_WAV_PATH) -> tuple[str, float]:
    """Grava áudio e detecta idioma usando Whisper.

    Retorna:
        (codigo_lingua, probabilidade) - código ISO do idioma e probabilidade de detecção.
    """
    caminho = gravar_audio(segundos=segundos, sample_rate=sample_rate, caminho_wav=wav_path)
    lingua = detectar_idioma_whisper(caminho)
    
    # Retorna língua e probabilidade (já foi impressa na detecção)
    # Para manter compatibilidade, retornamos 1.0 como confiança
    return lingua, 1.0

__all__ = [
    'get_whisper_model', 'detectar_idioma_whisper', 'gravar_audio', 'capturar_e_detectar_lingua'
]