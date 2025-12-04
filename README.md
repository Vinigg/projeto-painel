# Guia de Montagem: Sensor Ultrassônico e LEDs com Arduino

## 📦 **Materiais Necessários**
- 1 Placa Arduino (Uno, Mega ou similar)
- 1 Sensor ultrassônico HC-SR04
- 2 LEDs (1 verde, 1 vermelho)
- 2 Resistores de 1000Ω (marrom-preto-vermelho)
- 6 Jumpers (cabo macho-macho)
- 1 Protoboard (matriz de contatos)

---

## 🔌 **Passo 1: Preparando as Conexões da Protoboard**

1. **Conectar o GND da Protoboard:**
   - Insira um jumper conectando o pino **GND** do Arduino a uma **trilha lateral (barra negativa)** da protoboard (normalmente marcada com linha azul ou sinal "-").

2. **Conectar o 5V da Protoboard:**
   - Insira um jumper conectando o pino **5V** do Arduino à **outra trilha lateral (barra positiva)** da protoboard (normalmente marcada com linha vermelha ou sinal "+").

---

## 📡 **Passo 2: Conectar o Sensor Ultrassônico HC-SR04**

1. **Posicionar o sensor:**
   - Coloque o sensor HC-SR04 na área central da protoboard, atravessando o canal central, com os 4 pinos em direções opostas.

2. **Fazer as conexões:**
   - **Pino VCC do sensor** → Trilha positiva da protoboard (conectada ao 5V do Arduino)
   - **Pino GND do sensor** → Trilha negativa da protoboard (conectada ao GND do Arduino)
   - **Pino TRIG do sensor** → Pino 9 do Arduino (use jumper)
   - **Pino ECHO do sensor** → Pino 8 do Arduino (use jumper)

   *Nota: O pino TRIG envia o pulso, o ECHO recebe o retorno.*

---

## 💡 **Passo 3: Montar os LEDs com Resistores**

### Para o LED Verde:

1. **Posicionar o LED:**
   - Insira o LED verde na protoboard, com o **cátodo (perna curta)** na linha 7, coluna **e**.
   - O **ânodo (perna longa)** ficará na linha 7, coluna **f**.

2. **Adicionar o resistor:**
   - Coloque um resistor de 1000Ω (1kΩ) conectando:
     - Uma perna na linha 7, coluna **a** (trilha abcde)
     - Outra perna na linha 7, coluna **f** (trilha fghij)
   - *Isso conecta o resistor em série com o ânodo do LED.*

3. **Conectar ao Arduino e GND:**
   - Conecte um jumper do pino 7 do Arduino à linha 7, coluna **a** (mesmo ponto do resistor).
   - Conecte um jumper da trilha negativa (GND) à linha 7, coluna **e** (cátodo do LED).

### Para o LED Vermelho:

4. **Repetir o processo em outra linha:**
   - Use a linha 8 da protoboard para o LED vermelho.
   - Siga os mesmos passos, mas conecte o jumper do resistor ao **pino 6 do Arduino**.

---

## ✅ **Passo 4: Verificação Final**

| Componente | Pino no Arduino | Pino no Componente |
|------------|----------------|--------------------|
| Sensor | Pino 9 | TRIG |
| Sensor | Pino 8 | ECHO |
| Sensor | 5V | VCC |
| Sensor | GND | GND |
| LED Verde | Pino 7 | Ânodo (via resistor) |
| LED Vermelho | Pino 6 | Ânodo (via resistor) |
| Ambos LEDs | GND | Cátodo |

---

## 🔍 **Dicas Importantes:**

1. **Verifique a polaridade dos LEDs:** perna longa (ânodo = positivo), perna curta (cátodo = negativo)
2. **Os resistores são essenciais** para limitar a corrente e não queimar os LEDs
3. **Mantenha as conexões organizadas** para facilitar ajustes e correções
4. **Teste cada LED individualmente** antes de conectar o sensor

---

## 📝 **Diagrama de Conexão Simplificado:**

```
ARDUINO           PROTOBOARD          COMPONENTES
------           -----------          -----------
GND      ----->  Trilha (-)    -----> Sensor GND, LEDs (cátodo)
5V       ----->  Trilha (+)    -----> Sensor VCC
Pino 9   ----->                -----> Sensor TRIG
Pino 8   ----->                -----> Sensor ECHO
Pino 7   --resistor->          -----> LED Verde (ânodo)
Pino 6   --resistor->          -----> LED Vermelho (ânodo)
```

Agora seu circuito está pronto para receber o código de programação! 🚀
