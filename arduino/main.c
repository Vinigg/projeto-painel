const int sensorPIR = 2;
const int ledStatus = 13;
const int ledCaptura = 12;

void setup() {
  pinMode(sensorPIR, INPUT);
  pinMode(ledStatus, OUTPUT);
  pinMode(ledCaptura, OUTPUT);
  
  Serial.begin(9600);
  
  // Sinalizar inicialização
  digitalWrite(ledStatus, HIGH);
  delay(1000);
  digitalWrite(ledStatus, LOW);
  
  Serial.println("ARDUINO_PRONTO");
}

void loop() {
  // Verifica detecção de movimento
  if (digitalRead(sensorPIR) == HIGH) {
    Serial.println("PESSOA_DETECTADA");
    digitalWrite(ledStatus, HIGH);
    
    // Aguarda processamento do computador
    delay(10000); // Timeout de 10 segundos
    digitalWrite(ledStatus, LOW);
    
    // Debounce
    delay(5000);
  }
  
  // Verifica comandos do computador
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    
    processarComando(comando);
  }
  
  delay(100);
}

void processarComando(String comando) {
  if (comando == "CAPTURANDO") {
    // Piscar LED durante captura
    for (int i = 0; i < 10; i++) {
      digitalWrite(ledCaptura, HIGH);
      delay(500);
      digitalWrite(ledCaptura, LOW);
      delay(500);
    }
  }
  else if (comando.startsWith("LINGUA_")) {
    // Língua detectada - feedback visual
    digitalWrite(ledStatus, HIGH);
    delay(3000);
    digitalWrite(ledStatus, LOW);
  }
  else if (comando == "PRONTO") {
    // Sistema pronto para nova detecção
    digitalWrite(ledStatus, LOW);
    digitalWrite(ledCaptura, LOW);
  }
}