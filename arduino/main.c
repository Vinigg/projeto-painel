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

const float velocidadeSom = 0.00034029; // em metros por microsegundo

void setup(){
  
  pinMode(pinTrig, OUTPUT); 
  pinMode(pinEcho, INPUT); 
  pinMode(pinLed, OUTPUT);
  Serial.begin(9600); 

  digitalWrite(pinTrig, LOW);
  Serial.begin(9600);
}

void loop(){ 
  gatilhoSensor();
  tempoEcho = pulseIn(pinEcho, HIGH);
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

void gatilhoSensor(){  
    digitalWrite(pinTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrig, LOW);
}

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