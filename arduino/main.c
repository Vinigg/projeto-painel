// Projeto: Painel Inteligente com Sensor de Proximidade HC-SR04
// Sensor: HC-SR04 (Ultrassônico)
// Funcionalidade: Detectar aproximação de pessoas e comunicar com computador

// Definição dos pinos
const int trigPin = 9;      // Pino Trigger do HC-SR04
const int echoPin = 10;     // Pino Echo do HC-SR04
const int ledStatus = 13;   // LED indicador de status
const int ledCaptura = 12;  // LED indicador de captura de áudio

// Variáveis para controle
unsigned long ultimaDetecao = 0;
const unsigned long intervaloMinimo = 30000; // 30 segundos entre detecções
bool pessoaPresente = false;
const int distanciaLimite = 100; // Distância em cm para considerar presença

void setup() {
  // Configuração dos pinos
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledStatus, OUTPUT);
  pinMode(ledCaptura, OUTPUT);
  
  // Inicialização da comunicação serial
  Serial.begin(9600);
  
  // Sequência de inicialização
  sequenciaInicializacao();
  
  Serial.println("ARDUINO_PRONTO_HC_SR04");
  Serial.println("SISTEMA: Aguardando aproximação...");
}

void loop() {
  // Medir distância a cada 500ms
  long distancia = medirDistancia();
  
  // Verificar se há alguém próximo
  bool detecaoAtual = (distancia > 0 && distancia <= distanciaLimite);
  
  // Lógica de detecção com debounce
  if (detecaoAtual && !pessoaPresente) {
    if (podeDetectar()) {
      pessoaDetectada();
    }
  } 
  else if (!detecaoAtual && pessoaPresente) {
    pessoaSaiu();
  }
  
  // Feedback visual baseado no estado
  atualizarLEDs();
  
  // Processar comandos do computador
  processarComandosSerial();
  
  delay(500); // Intervalo entre medições
}

long medirDistancia() {
  /**
   * Mede a distância usando o sensor HC-SR04
   * Retorna a distância em centímetros
   */
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duracao = pulseIn(echoPin, HIGH, 30000); // Timeout de 30ms
  long distancia = duracao * 0.034 / 2;
  
  // Verificar se a medição é válida
  if (distancia <= 0 || distancia > 400) {
    return -1; // Medição inválida
  }
  
  return distancia;
}

bool podeDetectar() {
  /**
   * Verifica se pode realizar nova detecção
   * (evita múltiplas detecções rápidas)
   */
  unsigned long tempoAtual = millis();
  
  if (tempoAtual - ultimaDetecao >= intervaloMinimo) {
    ultimaDetecao = tempoAtual;
    return true;
  }
  
  return false;
}

void pessoaDetectada() {
  /**
   * Executado quando uma pessoa é detectada
   */
  pessoaPresente = true;
  Serial.println("PESSOA_DETECTADA");
  
  Serial.print("DISTANCIA: ");
  Serial.println(medirDistancia());
  
  // Feedback visual
  digitalWrite(ledStatus, HIGH);
  
  Serial.println("SISTEMA: Aguardando processamento do computador...");
}

void pessoaSaiu() {
  /**
   * Executado quando a pessoa se afasta
   */
  pessoaPresente = false;
  digitalWrite(ledStatus, LOW);
  Serial.println("PESSOA_SAIU");
}

void processarComandosSerial() {
  /**
   * Processa comandos recebidos do computador
   */
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    
    Serial.print("COMANDO_RECEBIDO: ");
    Serial.println(comando);
    
    executarComando(comando);
  }
}

void executarComando(String comando) {
  /**
   * Executa ação baseada no comando recebido
   */
  if (comando == "CAPTURANDO") {
    modoCapturaAudio();
  }
  else if (comando.startsWith("LINGUA_")) {
    linguaDetectada(comando);
  }
  else if (comando == "PRONTO") {
    modoPronto();
  }
  else if (comando == "ERRO_PROCESSAMENTO") {
    modoErro();
  }
  else if (comando == "AUDIO_NAO_CAPTURADO") {
    modoAudioNaoCapturado();
  }
  else if (comando == "LINGUA_DESCONHECIDA") {
    modoLinguaDesconhecida();
  }
}

void modoCapturaAudio() {
  /**
   * Modo: Capturando áudio do usuário
   */
  Serial.println("MODO: Capturando áudio");
  
  // Piscar LED de captura rapidamente
  for (int i = 0; i < 6; i++) {
    digitalWrite(ledCaptura, HIGH);
    delay(300);
    digitalWrite(ledCaptura, LOW);
    delay(300);
  }
}

void linguaDetectada(String comando) {
  /**
   * Modo: Língua detectada com sucesso
   */
  String lingua = comando.substring(7); // Remove "LINGUA_"
  
  Serial.print("LINGUA_IDENTIFICADA: ");
  Serial.println(lingua);
  
  // Feedback visual - piscar LEDs em sequência
  for (int i = 0; i < 3; i++) {
    digitalWrite(ledStatus, HIGH);
    digitalWrite(ledCaptura, HIGH);
    delay(200);
    digitalWrite(ledStatus, LOW);
    digitalWrite(ledCaptura, LOW);
    delay(200);
  }
}

void modoPronto() {
  /**
   * Modo: Sistema pronto para nova detecção
   */
  Serial.println("SISTEMA: Pronto para nova detecção");
  digitalWrite(ledStatus, LOW);
  digitalWrite(ledCaptura, LOW);
  pessoaPresente = false;
}

void modoErro() {
  /**
   * Modo: Erro no processamento
   */
  Serial.println("ERRO: Falha no processamento");
  
  // Feedback de erro - LEDs piscam alternadamente
  for (int i = 0; i < 4; i++) {
    digitalWrite(ledStatus, HIGH);
    digitalWrite(ledCaptura, LOW);
    delay(250);
    digitalWrite(ledStatus, LOW);
    digitalWrite(ledCaptura, HIGH);
    delay(250);
  }
}

void modoAudioNaoCapturado() {
  /**
   * Modo: Áudio não foi capturado
   */
  Serial.println("AVISO: Áudio não capturado");
  
  // Feedback - LED de captura pisca lentamente
  for (int i = 0; i < 2; i++) {
    digitalWrite(ledCaptura, HIGH);
    delay(1000);
    digitalWrite(ledCaptura, LOW);
    delay(500);
  }
}

void modoLinguaDesconhecida() {
  /**
   * Modo: Língua não identificada
   */
  Serial.println("AVISO: Língua não identificada");
  
  // Feedback - LED de status pisca lentamente
  for (int i = 0; i < 2; i++) {
    digitalWrite(ledStatus, HIGH);
    delay(1000);
    digitalWrite(ledStatus, LOW);
    delay(500);
  }
}

void atualizarLEDs() {
  /**
   * Atualiza os LEDs baseado no estado atual
   */
  static unsigned long ultimoPisca = 0;
  static bool estadoPisca = false;
  
  // Se pessoa está presente, LED status fica acesso
  // Se não, pisca lentamente indicando sistema ativo
  if (pessoaPresente) {
    digitalWrite(ledStatus, HIGH);
  } else {
    // Piscar a cada 2 segundos quando em espera
    if (millis() - ultimoPisca >= 2000) {
      ultimoPisca = millis();
      estadoPisca = !estadoPisca;
      digitalWrite(ledStatus, estadoPisca ? HIGH : LOW);
    }
  }
}

void sequenciaInicializacao() {
  /**
   * Sequência de inicialização dos LEDs
   */
  for (int i = 0; i < 3; i++) {
    digitalWrite(ledStatus, HIGH);
    digitalWrite(ledCaptura, HIGH);
    delay(200);
    digitalWrite(ledStatus, LOW);
    digitalWrite(ledCaptura, LOW);
    delay(200);
  }
  
  digitalWrite(ledStatus, HIGH);
  delay(1000);
  digitalWrite(ledStatus, LOW);
}

// Função para debug (opcional)
void debugDistancia() {
  /**
   * Função para debug das medições de distância
   * (Chamar no loop se necessário para testes)
   */
  static unsigned long ultimoDebug = 0;
  
  if (millis() - ultimoDebug >= 5000) { // A cada 5 segundos
    ultimoDebug = millis();
    long dist = medirDistancia();
    
    Serial.print("DEBUG_DISTANCIA: ");
    Serial.print(dist);
    Serial.println(" cm");
    
    Serial.print("PESSOA_PRESENTE: ");
    Serial.println(pessoaPresente ? "SIM" : "NAO");
  }
}
