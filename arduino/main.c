/*******************************************************************************
*
*    I15 - Usando sensor ultrassônico sem biblioteca
*    Autor: Angelo Luis Ferreira
*    28/02/2022
*    http://squids.com.br/arduino
*
*******************************************************************************/
int pinLed = 7;
int pinTrig = 9; // pino usado para disparar os pulsos do sensor
int pinEcho = 8; // pino usado para ler a saida do sensor
float tempoEcho = 0;
// Obs. Velocidade do som = 340,29 m/s = 0.00034029 m/us
const float velocidadeSom = 0.00034029; // em metros por microsegundo

void setup(){
  // Configura pinos Trig e Echo
  pinMode(pinTrig, OUTPUT); // configura pino TRIG como saída
  pinMode(pinEcho, INPUT); // configura pino ECHO como entrada
  pinMode(pinLed, OUTPUT);
  Serial.begin(9600); 

  // Inicializa pino Trig em nível baixo
  digitalWrite(pinTrig, LOW);
  
  // Inicializa a porta serial
  Serial.begin(9600);
}

void loop(){ 
  gatilhoSensor(); // envia pulso trigger (gatilho) para disparar o sensor  
  tempoEcho = pulseIn(pinEcho, HIGH); // mede o tempo de duração do sinal no pino de leitura em us
  // exibe no monitor serial
  Serial.print("Distancia em metros: ");
  Serial.println(calculaDistancia(tempoEcho), 4);
  Serial.print("Distancia em centimetros: ");
  Serial.println(calculaDistancia(tempoEcho)*100);
  Serial.println("------------------------------------");
  if(calculaDistancia(tempoEcho)*100 <= 30){
    enviarMensagem("Arduino iniciado!");
    Serial.print("Pessoa detectada");
    ligarled();
  }
  
  delay(2000); // aguarda dois segundos
}

// Funçao para enviar o pulso de trigger
void  gatilhoSensor(){
  // Para fazer o HC-SR04 enviar um pulso ultrassonico, nos temos
  // que enviar para o pino de trigger um sinal de nivel alto
  // com pelo menos 10us de duraçao
  digitalWrite(pinTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrig, LOW);
}


// Função para calcular a distancia em metros
float calculaDistancia(float tempoMicrossegundos){
  return((tempoMicrossegundos*velocidadeSom)/2); // velocidade do som em m/microssegundo
}

void ligarled(){
  digitalWrite(pinLed, HIGH);
  delay(5000);
  digitalWrite(pinLed, LOW);
}

void enviarMensagem(const char* msg) {
    Serial.println(msg);   // envia o texto
}