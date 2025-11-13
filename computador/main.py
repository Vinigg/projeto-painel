import serial
import speech_recognition as sr
import pygame
import os
import time
import threading
from langdetect import detect
import json

class PainelInteligente:
    def __init__(self):
        # Configurações
        self.config = {
            'serial_port': 'COM3',  # Linux: '/dev/ttyUSB0'
            'baud_rate': 9600,
            'linguas_suportadas': ['pt', 'en', 'es', 'fr', 'de'],
            'tempo_captura': 5,
            'pasta_imagens': 'imagens/',
            'tempo_exibicao': 30
        }
        
        # Inicializações
        self.serial_conn = None
        self.reconhecedor = sr.Recognizer()
        self.microfone = sr.Microphone()
        self.tela_ativa = False
        
        # Estado do sistema
        self.estado = "aguardando"
        self.lingua_detectada = None
        
        self.inicializar_sistema()
    
    def inicializar_sistema(self):
        """Inicializa todos os componentes do sistema"""
        try:
            # Conectar com Arduino
            self.conectar_arduino()
            
            # Inicializar pygame para exibição de imagens
            pygame.init()
            self.tela = pygame.display.set_mode((800, 600))
            pygame.display.set_caption("Painel Inteligente")
            
            # Calibrar microfone
            print("Calibrando microfone para ruído ambiente...")
            with self.microfone as source:
                self.reconhecedor.adjust_for_ambient_noise(source)
            
            print("✅ Sistema inicializado e pronto!")
            
        except Exception as e:
            print(f"❌ Erro na inicialização: {e}")
    
    def conectar_arduino(self):
        """Estabelece conexão serial com Arduino"""
        try:
            self.serial_conn = serial.Serial(
                self.config['serial_port'],
                self.config['baud_rate'],
                timeout=1
            )
            time.sleep(2)  # Aguarda Arduino inicializar
            print("✅ Conectado ao Arduino")
        except Exception as e:
            print(f"❌ Erro ao conectar com Arduino: {e}")
    
    def enviar_para_arduino(self, comando):
        """Envia comando para Arduino"""
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write(f"{comando}\n".encode())
                print(f"📤 Enviado para Arduino: {comando}")
            except Exception as e:
                print(f"❌ Erro ao enviar comando: {e}")
    
    def ler_do_arduino(self):
        """Lê dados do Arduino de forma não-bloqueante"""
        if self.serial_conn and self.serial_conn.in_waiting > 0:
            try:
                linha = self.serial_conn.readline().decode().strip()
                if linha:
                    print(f"📥 Recebido do Arduino: {linha}")
                    return linha
            except Exception as e:
                print(f"❌ Erro ao ler do Arduino: {e}")
        return None
    
    def capturar_audio(self):
        """Captura áudio do microfone e converte para texto"""
        try:
            print("🎤 Capturando áudio... Fale agora!")
            
            with self.microfone as source:
                # Captura áudio com timeout
                audio = self.reconhecedor.listen(source, timeout=10, phrase_time_limit=self.config['tempo_captura'])
            
            print("🔍 Processando reconhecimento de voz...")
            
            # Reconhece usando Google Speech Recognition
            texto = self.reconhecedor.recognize_google(audio, language='pt-BR')
            print(f"📝 Texto detectado: {texto}")
            
            return texto
            
        except sr.WaitTimeoutError:
            print("⏰ Tempo de captura expirado")
            return None
        except sr.UnknownValueError:
            print("❌ Não foi possível entender o áudio")
            return None
        except sr.RequestError as e:
            print(f"❌ Erro no serviço de reconhecimento: {e}")
            return None
    
    def detectar_lingua(self, texto):
        """Detecta a língua do texto falado"""
        try:
            if texto:
                lingua = detect(texto)
                print(f"🌐 Língua detectada: {lingua}")
                return lingua
            return None
        except Exception as e:
            print(f"❌ Erro na detecção de língua: {e}")
            return None
    
    def exibir_imagem(self, lingua):
        """Exibe a imagem correspondente à língua detectada"""
        try:
            caminho_imagem = f"{self.config['pasta_imagens']}{lingua}.jpg"
            
            # Verifica se arquivo existe, senão usa padrão
            if not os.path.exists(caminho_imagem):
                caminho_imagem = f"{self.config['pasta_imagens']}default.jpg"
            
            if os.path.exists(caminho_imagem):
                imagem = pygame.image.load(caminho_imagem)
                imagem = pygame.transform.scale(imagem, (800, 600))
                self.tela.blit(imagem, (0, 0))
                pygame.display.flip()
                print(f"🖼️ Exibindo imagem para língua: {lingua}")
                
                # Mantém a imagem exibida por tempo determinado
                time.sleep(self.config['tempo_exibicao'])
                
                # Limpa a tela
                self.tela.fill((0, 0, 0))
                pygame.display.flip()
                
            else:
                print(f"❌ Arquivo de imagem não encontrado: {caminho_imagem}")
                
        except Exception as e:
            print(f"❌ Erro ao exibir imagem: {e}")
    
    def processar_interacao(self):
        """Processa uma interação completa do usuário"""
        if self.estado != "aguardando":
            return
        
        self.estado = "processando"
        print("\n" + "="*50)
        print("🚀 INICIANDO NOVA INTERAÇÃO")
        print("="*50)
        
        try:
            # Passo 1: Sinalizar que está capturando áudio
            self.enviar_para_arduino("CAPTURANDO")
            
            # Passo 2: Capturar áudio
            texto = self.capturar_audio()
            
            if texto:
                # Passo 3: Detectar língua
                lingua = self.detectar_lingua(texto)
                
                if lingua and lingua in self.config['linguas_suportadas']:
                    self.lingua_detectada = lingua
                    
                    # Passo 4: Sinalizar língua detectada
                    self.enviar_para_arduino(f"LINGUA_{lingua.upper()}")
                    
                    # Passo 5: Exibir imagem
                    self.exibir_imagem(lingua)
                    
                    print(f"✅ Interação concluída - Língua: {lingua}")
                else:
                    print("❌ Língua não suportada ou não detectada")
                    self.enviar_para_arduino("LINGUA_DESCONHECIDA")
                    self.exibir_imagem("default")
            else:
                print("❌ Nenhum áudio capturado")
                self.enviar_para_arduino("AUDIO_NAO_CAPTURADO")
                self.exibir_imagem("default")
                
        except Exception as e:
            print(f"❌ Erro no processamento: {e}")
            self.enviar_para_arduino("ERRO_PROCESSAMENTO")
        
        finally:
            self.estado = "aguardando"
            self.enviar_para_arduino("PRONTO")
            print("🔄 Sistema pronto para nova interação\n")
    
    def executar(self):
        """Loop principal do sistema"""
        print("🎯 Sistema em execução. Aguardando sinal do Arduino...")
        
        try:
            while True:
                # Verifica se há comunicação do Arduino
                mensagem = self.ler_do_arduino()
                
                if mensagem == "PESSOA_DETECTADA" and self.estado == "aguardando":
                    # Inicia processamento em thread separada para não bloquear
                    thread = threading.Thread(target=self.processar_interacao)
                    thread.daemon = True
                    thread.start()
                
                # Processa eventos do pygame (mantém a janela responsiva)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                
                time.sleep(0.1)  # Evita uso excessivo de CPU
                
        except KeyboardInterrupt:
            print("\n🛑 Sistema interrompido pelo usuário")
        finally:
            self.fechar_sistema()
    
    def fechar_sistema(self):
        """Fecha todos os recursos do sistema"""
        print("🔒 Fechando recursos...")
        if self.serial_conn:
            self.serial_conn.close()
        pygame.quit()

# Execução principal
if __name__ == "__main__":
    painel = PainelInteligente()
    painel.executar()