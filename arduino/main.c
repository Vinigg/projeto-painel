int pinGreenLed = 7; // pino do led verde
int pinRedLed = 6; // pino do led vermelho
int pinTrig = 9; // pino usado para disparar os pulsos do sensor
int pinEcho = 8; // pino usado para ler a saida do sensor
float tempoEcho = 0;

const float velocidadeSom = 0.00034029; // em metros por microsegundo

void setup(){
  
  pinMode(pinTrig, OUTPUT); 
  pinMode(pinEcho, INPUT); 
  pinMode(pinGreenLed, OUTPUT);
  pinMode(pinRedLed, OUTPUT);
  Serial.begin(9600); 

  digitalWrite(pinTrig, LOW);
  digitalWrite(pinGreenLed, LOW);
  digitalWrite(pinRedLed, LOW);
}

void loop(){ 
  // Verifica se há dados disponíveis na porta serial
  if(Serial.available() > 0){
    String mensagem = Serial.readStringUntil('\n');
    mensagem.trim(); // Remove espaços em branco e quebras de linha
    
    if(mensagem.equalsIgnoreCase("erro")){
      piscarLedVermelho(5000); // Pisca o LED vermelho por 5 segundos
    }
  }
  
  gatilhoSensor();
  tempoEcho = pulseIn(pinEcho, HIGH);
  Serial.print("Distancia em metros: "); 
  Serial.println(calculaDistancia(tempoEcho), 4); 
  Serial.print("Distancia em centimetros: "); 
  Serial.println(calculaDistancia(tempoEcho)*100); 
  Serial.println("------------------------------------"); 
  
  if(calculaDistancia(tempoEcho)*100 <= 30){ 
    enviarMensagem("Arduino iniciado!"); 
    Serial.print("evento"); 
    ligarled(); 
  }
  
  delay(2000); // aguarda dois segundos
}

void gatilhoSensor(){  
  digitalWrite(pinTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrig, LOW);
}

float calculaDistancia(float tempoMicrossegundos){
  return((tempoMicrossegundos*velocidadeSom)/2); // velocidade do som em m/microssegundo
}

void ligarled(){
  digitalWrite(pinGreenLed, HIGH);
  delay(5000);
  digitalWrite(pinGreenLed, LOW);
}

void piscarLedVermelho(int duracaoMs){
  unsigned long inicio = millis();
  unsigned long fim = inicio + duracaoMs;
  bool estadoLed = LOW;
  
  while(millis() < fim){
    digitalWrite(pinRedLed, estadoLed);
    estadoLed = !estadoLed; // Alterna o estado do LED
    delay(250); // Pisca a cada 250ms (4 vezes por segundo)
  }
  
  digitalWrite(pinRedLed, LOW); // Garante que o LED fique apagado ao final
}

void enviarMensagem(const char* msg) {
  Serial.println(msg); // envia o texto
}