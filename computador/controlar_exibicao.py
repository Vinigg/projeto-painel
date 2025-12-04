import pygame
import os
import sys
import time
from datetime import datetime
import json

class ControladorExibicao:
    def __init__(self, config_path="config_exibicao.json"):
        # Carregar configurações
        self.config = self.carregar_configuracoes(config_path)
        
        # Inicializar pygame
        self.inicializar_pygame()
        
        # Estado do sistema
        self.tela_ativa = False
        self.imagem_atual = None
        self.tempo_inicio_exibicao = None
        self.lingua_atual = None
        
        # Imagem default
        self.imagem_default = None
        self.dimensoes_default = None
        self._ultima_foi_fallback = False
        
        # Estatísticas
        self.estatisticas = {
            'total_exibicoes': 0,
            'exibicoes_por_lingua': {},
            'ultima_lingua': None,
            'tempo_total_exibicao': 0
        }
        
        print("✅ Controlador de exibição inicializado")
        
        # Carregar e exibir imagem default
        self.carregar_imagem_default()
        self.exibir_default()
    
    def carregar_configuracoes(self, config_path):
        """Carrega configurações do arquivo JSON"""
        config_padrao = {
            "largura_tela": 800,
            "altura_tela": 600,
            "pasta_imagens": "images",
            "tempo_exibicao": 30,
            "cor_fundo": [0, 0, 0],
            "tela_cheia": False,
            "linguas_suportadas": ["pt", "en", "es", "fr", "de", "it"],
            "imagem_default": "default.jpg",
            "imagem_erro": "erro.jpg",
            "log_estatisticas": True
        }
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_usuario = json.load(f)
                
                # Mesclar configurações
                config_padrao.update(config_usuario)
                print("✅ Configurações carregadas do arquivo")
            else:
                # Criar arquivo de configuração padrão
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(config_padrao, f, indent=4, ensure_ascii=False)
                print("📁 Arquivo de configuração criado")
                
        except Exception as e:
            print(f"⚠️ Erro ao carregar configurações: {e}. Usando padrões.")
        
        return config_padrao
    
    def inicializar_pygame(self):
        """Inicializa o Pygame e configura a tela"""
        try:
            pygame.init()
            
            # Configurar tela
            if self.config['tela_cheia']:
                self.tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                info_tela = pygame.display.Info()
                self.config['largura_tela'] = info_tela.current_w
                self.config['altura_tela'] = info_tela.current_h
            else:
                self.tela = pygame.display.set_mode(
                    (self.config['largura_tela'], self.config['altura_tela'])
                )
            
            pygame.display.set_caption("Painel Inteligente - Sistema de Propaganda")
            self.fonte = pygame.font.Font(None, 36)
            
            print(f"🖥️ Tela configurada: {self.config['largura_tela']}x{self.config['altura_tela']}")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar Pygame: {e}")
            sys.exit(1)
    
    def carregar_imagem_default(self):
        """Carrega a imagem default que será exibida quando não houver propaganda"""
        tentativas = [
            'default.jpeg',
            'default.jpg',
            'default.png',
            self.config['imagem_default']
        ]
        
        for nome_arquivo in tentativas:
            caminho_imagem = os.path.join(self.config['pasta_imagens'], nome_arquivo)
            
            if os.path.exists(caminho_imagem):
                try:
                    imagem = pygame.image.load(caminho_imagem)
                    print(f"✅ Imagem default carregada: {caminho_imagem}")
                    self.imagem_default, self.dimensoes_default = self.redimensionar_imagem(imagem)
                    return
                except Exception as e:
                    print(f"❌ Erro ao carregar {caminho_imagem}: {e}")
                    continue
        
        # Se não encontrou imagem default, criar uma
        print("⚠️ Nenhuma imagem default encontrada, criando tela preta")
        self.imagem_default, self.dimensoes_default = self.criar_tela_default()
    
    def criar_tela_default(self):
        """Cria uma tela default simples quando não há imagem"""
        largura, altura = self.config['largura_tela'], self.config['altura_tela']
        superficie = pygame.Surface((largura, altura))
        superficie.fill(self.config['cor_fundo'])
        
        # Adicionar texto informativo
        texto = "Sistema Pronto - Aguardando Detecção"
        texto_surface = self.fonte.render(texto, True, (100, 100, 100))
        texto_rect = texto_surface.get_rect(center=(largura//2, altura//2))
        superficie.blit(texto_surface, texto_rect)
        
        return superficie, (largura, altura)
    
    def exibir_default(self):
        """Exibe a imagem default na tela"""
        if not self.imagem_default:
            return
        
        # Limpar estado
        self.tela_ativa = False
        self.imagem_atual = None
        self.lingua_atual = None
        self.tempo_inicio_exibicao = None
        
        # Limpar tela
        self.tela.fill(self.config['cor_fundo'])
        
        # Centralizar e exibir imagem default
        x = (self.config['largura_tela'] - self.dimensoes_default[0]) // 2
        y = (self.config['altura_tela'] - self.dimensoes_default[1]) // 2
        self.tela.blit(self.imagem_default, (x, y))
        
        pygame.display.flip()
        print("🏠 Exibindo tela default")
    
    def exibir_captando(self):
        """Exibe a imagem 'captando' durante a gravação de áudio"""
        print("🎙️ Exibindo tela de captura...")
        
        # Tentar carregar imagem específica de captura
        tentativas = [
            'captando.jpeg',
            'captando.jpg',
            'captando.png',
            'recording.jpg'
        ]
        
        imagem_captando = None
        for nome_arquivo in tentativas:
            caminho_imagem = os.path.join(self.config['pasta_imagens'], nome_arquivo)
            if os.path.exists(caminho_imagem):
                try:
                    imagem = pygame.image.load(caminho_imagem)
                    imagem_captando, dimensoes = self.redimensionar_imagem(imagem)
                    print(f"✅ Imagem de captura carregada: {caminho_imagem}")
                    break
                except Exception as e:
                    print(f"❌ Erro ao carregar {caminho_imagem}: {e}")
                    continue
        
        # Se não encontrou imagem, criar uma com texto
        if imagem_captando is None:
            largura, altura = self.config['largura_tela'], self.config['altura_tela']
            imagem_captando = pygame.Surface((largura, altura))
            imagem_captando.fill(self.config['cor_fundo'])
            
            # Adicionar texto informativo
            textos = [
                "🎤 Gravando Áudio...",
                "Por favor, fale seu idioma"
            ]
            
            fonte_grande = pygame.font.Font(None, 72)
            fonte_media = pygame.font.Font(None, 48)
            
            for i, texto in enumerate(textos):
                fonte = fonte_grande if i == 0 else fonte_media
                texto_surface = fonte.render(texto, True, (255, 255, 255))
                texto_rect = texto_surface.get_rect(center=(largura//2, altura//2 - 50 + i*80))
                imagem_captando.blit(texto_surface, texto_rect)
            
            dimensoes = (largura, altura)
            print("📝 Imagem de captura criada com texto")
        
        # Limpar tela e exibir
        self.tela.fill(self.config['cor_fundo'])
        x = (self.config['largura_tela'] - dimensoes[0]) // 2
        y = (self.config['altura_tela'] - dimensoes[1]) // 2
        self.tela.blit(imagem_captando, (x, y))
        pygame.display.flip()
    
    def carregar_imagem(self, lingua):
        """
        Carrega a imagem correspondente à língua
        Retorna a imagem redimensionada ou None se não encontrada
        """
        # Mapear códigos de língua para nomes de arquivo
        mapeamento_arquivos = {
            'pt': 'portugues.jpg',
            'en': 'ingles.jpg', 
            'es': 'espanhol.jpg',
            'fr': 'frances.jpg',
            'de': 'alemao.jpg',
            'it': 'italiano.jpg'
        }
        
        # Tentar diferentes nomes de arquivo
        tentativas = [
            f"{lingua}.jpg",
            f"{lingua}.png",
            mapeamento_arquivos.get(lingua, f"{lingua}.jpg"),
            self.config['imagem_default']
        ]
        
        self._ultima_foi_fallback = False
        for nome_arquivo in tentativas:
            caminho_imagem = os.path.join(self.config['pasta_imagens'], nome_arquivo)
            
            if os.path.exists(caminho_imagem):
                try:
                    imagem = pygame.image.load(caminho_imagem)
                    print(f"✅ Imagem carregada: {caminho_imagem}")
                    return self.redimensionar_imagem(imagem)
                except Exception as e:
                    print(f"❌ Erro ao carregar {caminho_imagem}: {e}")
                    continue
        
        # Se nenhuma imagem foi encontrada
        print(f"❌ Nenhuma imagem encontrada para a língua: {lingua}")
        self._ultima_foi_fallback = True
        return self.criar_imagem_fallback(lingua)
    
    def redimensionar_imagem(self, imagem):
        """Redimensiona a imagem para caber na tela mantendo a proporção"""
        largura_original, altura_original = imagem.get_size()
        largura_tela, altura_tela = self.config['largura_tela'], self.config['altura_tela']
        
        # Calcular proporção
        proporcao_largura = largura_tela / largura_original
        proporcao_altura = altura_tela / altura_original
        proporcao = min(proporcao_largura, proporcao_altura)
        
        # Calcular novas dimensões
        nova_largura = int(largura_original * proporcao)
        nova_altura = int(altura_original * proporcao)
        
        # Redimensionar
        imagem_redimensionada = pygame.transform.smoothscale(imagem, (nova_largura, nova_altura))
        
        return imagem_redimensionada, (nova_largura, nova_altura)
    
    def criar_imagem_fallback(self, lingua):
        """Cria uma imagem de fallback quando não encontra o arquivo"""
        largura, altura = self.config['largura_tela'], self.config['altura_tela']
        superficie = pygame.Surface((largura, altura))
        
        # Cor de fundo
        superficie.fill(self.config['cor_fundo'])
        
        # Texto informativo
        textos = [
            f"Propaganda em {self.obter_nome_lingua(lingua)}",
            "Conteúdo não disponível",
            "Entre em contato com o administrador"
        ]
        
        for i, texto in enumerate(textos):
            texto_surface = self.fonte.render(texto, True, (255, 255, 255))
            texto_rect = texto_surface.get_rect(center=(largura//2, altura//2 - 50 + i*50))
            superficie.blit(texto_surface, texto_rect)
        
        print(f"🔄 Imagem fallback criada para: {lingua}")
        return superficie, (largura, altura)
    
    def obter_nome_lingua(self, codigo_lingua):
        """Retorna o nome completo da língua"""
        nomes = {
            'pt': 'Português',
            'en': 'Inglês',
            'es': 'Espanhol',
            'fr': 'Francês',
            'de': 'Alemão',
            'it': 'Italiano',
            'desconhecida': 'Desconhecida',
            'erro': 'Erro'
        }
        return nomes.get(codigo_lingua, codigo_lingua)
    
    def exibir_imagem_lingua(self, lingua):
        """
        Exibe a imagem correspondente à língua detectada
        """
        if self.tela_ativa:
            print("⚠️ Tela já está exibindo conteúdo. Ignorando comando.")
            return False
        
        self.lingua_atual = lingua
        self.tela_ativa = True
        self.tempo_inicio_exibicao = time.time()
        
        print(f"🎯 Exibindo propaganda em: {self.obter_nome_lingua(lingua)}")
        
        # Carregar imagem
        self.imagem_atual, self.dimensoes_imagem = self.carregar_imagem(lingua)
        
        # Atualizar estatísticas
        self.atualizar_estatisticas(lingua)
        
        # Exibir imagem
        self.atualizar_tela()
        
        # Retorna False se foi necessário usar fallback (tratado como erro pelo orquestrador)
        return not self._ultima_foi_fallback
    
    def atualizar_tela(self):
        """Atualiza o conteúdo da tela"""
        # Limpar tela
        self.tela.fill(self.config['cor_fundo'])
        
        if self.imagem_atual:
            # Centralizar imagem
            x = (self.config['largura_tela'] - self.dimensoes_imagem[0]) // 2
            y = (self.config['altura_tela'] - self.dimensoes_imagem[1]) // 2
            self.tela.blit(self.imagem_atual, (x, y))
        
        # Adicionar overlay informativo (opcional)
        if self.config.get('mostrar_info', True):
            self.desenhar_overlay()
        
        pygame.display.flip()
    
    def desenhar_overlay(self):
        """Desenha informações sobrepostas na tela"""
        # Tempo restante
        if self.tempo_inicio_exibicao:
            tempo_decorrido = time.time() - self.tempo_inicio_exibicao
            tempo_restante = max(0, self.config['tempo_exibicao'] - tempo_decorrido)
            
            texto_tempo = f"Tempo restante: {int(tempo_restante)}s"
            superficie_tempo = self.fonte.render(texto_tempo, True, (255, 255, 255))
            self.tela.blit(superficie_tempo, (20, 20))
        
        # Língua atual
        if self.lingua_atual:
            texto_lingua = f"Idioma: {self.obter_nome_lingua(self.lingua_atual)}"
            superficie_lingua = self.fonte.render(texto_lingua, True, (255, 255, 255))
            self.tela.blit(superficie_lingua, (20, 60))
    
    def atualizar_estatisticas(self, lingua):
        """Atualiza as estatísticas de exibição"""
        self.estatisticas['total_exibicoes'] += 1
        self.estatisticas['ultima_lingua'] = lingua
        
        if lingua in self.estatisticas['exibicoes_por_lingua']:
            self.estatisticas['exibicoes_por_lingua'][lingua] += 1
        else:
            self.estatisticas['exibicoes_por_lingua'][lingua] = 1
        
        # Salvar estatísticas periodicamente
        if self.estatisticas['total_exibicoes'] % 10 == 0:
            self.salvar_estatisticas()
    
    def salvar_estatisticas(self):
        """Salva estatísticas em arquivo JSON"""
        if self.config['log_estatisticas']:
            try:
                with open('estatisticas_exibicao.json', 'w', encoding='utf-8') as f:
                    json.dump(self.estatisticas, f, indent=4, ensure_ascii=False)
                print("📊 Estatísticas salvas")
            except Exception as e:
                print(f"❌ Erro ao salvar estatísticas: {e}")
    
    def verificar_tempo_exibicao(self):
        """
        Verifica se o tempo de exibição expirou
        Retorna True se deve continuar exibindo, False se deve parar
        """
        if not self.tela_ativa or not self.tempo_inicio_exibicao:
            return False
        
        tempo_decorrido = time.time() - self.tempo_inicio_exibicao
        
        if tempo_decorrido >= self.config['tempo_exibicao']:
            print("⏰ Tempo de exibição concluído")
            self.encerrar_exibicao()
            return False
        
        return True
    
    def encerrar_exibicao(self):
        """Encerra a exibição atual e retorna para a tela default"""
        print("🔄 Encerrando propaganda - Retornando para tela default")
        self.exibir_default()
    
    def processar_eventos(self):
        """Processa eventos do Pygame (teclado, mouse, etc.)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("⎋ Escape pressionado - Encerrando exibição")
                    self.encerrar_exibicao()
                    return True
                elif event.key == pygame.K_q:
                    print("👋 Tecla Q pressionada - Saindo do programa")
                    return False
                elif event.key == pygame.K_SPACE and self.tela_ativa:
                    print("⏭️ Espaço pressionado - Pulando exibição atual")
                    self.encerrar_exibicao()
        
        return True
    
    def executar_loop(self):
        """
        Loop principal de execução
        Use esta função se quiser que o controlador rode independentemente
        """
        print("🎬 Iniciando loop principal de exibição...")
        print("Controles: ESC - Encerrar exibição | Q - Sair | ESPAÇO - Pular")
        
        executando = True
        clock = pygame.time.Clock()
        
        while executando:
            # Processar eventos
            executando = self.processar_eventos()
            
            # Verificar tempo de exibição
            if self.tela_ativa:
                self.verificar_tempo_exibicao()
                self.atualizar_tela()
            
            clock.tick(30)  # 30 FPS
        
        self.encerrar()
    
    def encerrar(self):
        """Encerra o controlador de exibição"""
        print("🔴 Encerrando controlador de exibição...")
        self.salvar_estatisticas()
        pygame.quit()

# Funções de interface simples
def criar_estrutura_pastas():
    """Cria a estrutura de pastas necessária"""
    pastas = ['imagens', 'logs', 'config']
    
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)
    
    # Criar imagens padrão de exemplo
    imagens_padrao = {
        'pt': 'portugues.jpg',
        'en': 'ingles.jpg', 
        'es': 'espanhol.jpg',
        'default': 'default.jpg',
        'erro': 'erro.jpg'
    }
    
    print("📁 Estrutura de pastas criada")
    print("⚠️ Lembre-se de adicionar suas imagens na pasta 'imagens/'")

# Exemplo de uso
if __name__ == "__main__":
    # Criar estrutura de pastas
    criar_estrutura_pastas()
    
    # Inicializar controlador
    controlador = ControladorExibicao()
    
    # Exemplo: simular detecção de línguas
    print("\n🧪 Modo de teste - Simulando detecções:")
    
    # Testar com diferentes línguas
    linguas_teste = ['pt', 'en', 'es', 'fr', 'desconhecida']
    
    for lingua in linguas_teste:
        input(f"\nPressione Enter para testar língua: {lingua}")
        controlador.exibir_imagem_lingua(lingua)
        
        # Manter exibição por alguns segundos
        tempo_inicio = time.time()
        while time.time() - tempo_inicio < 5:  # 5 segundos de teste
            if not controlador.processar_eventos():
                break
            controlador.verificar_tempo_exibicao()
            time.sleep(0.1)
    
    controlador.encerrar()