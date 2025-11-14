# # import serial


# # ser = serial.Serial('COM11', 9600)  # Porta e baudrate

# # while True:
# #     dado = ser.readline().decode().strip()
# #     print("Recebido:", dado)

# import serial
# import time

# while True:
#     try:
#         ser = serial.Serial('COM17', 9600, timeout=1)
#         print("Conectado com sucesso!")
#         break
#     except serial.SerialException as e:
#         print("Erro ao abrir porta COM17:", e)
#         print("Tentando novamente em 2 segundos...")
#         time.sleep(2)

# while True:
#     try:
#         dado = ser.readline().decode().strip()
#         if dado:
#             print("Recebido:", dado)
#     except Exception as e:
#         print("Erro na leitura:", e)
#         break


# import serial.tools.list_ports

# def encontrar_arduino():
#     portas = serial.tools.list_ports.comports()
#     for porta in portas:
#         if ("Arduino" in porta.description or 
#             "CH340" in porta.description or 
#             "USB-SERIAL" in porta.description or
#             "CP210" in porta.description):
#             return porta.device
#     return None

# porta = encontrar_arduino()

# if porta is None:
#     print("Nenhum Arduino encontrado.")
# else:
#     print("Arduino encontrado em:", porta)


import serial
import serial.tools.list_ports
import time

def encontrar_arduino():
    portas = serial.tools.list_ports.comports()

    for porta in portas:
        desc = porta.description.lower()

        if ("arduino" in desc or
            "ch340" in desc or
            "usb-serial" in desc or
            "cp210" in desc):
            print(f"Arduino encontrado em: {porta.device}")
            return porta.device

    return None

# Tenta encontrar a porta do Arduino
porta_arduino = encontrar_arduino()

if porta_arduino is None:
    print("Nenhum Arduino encontrado. Verifique o cabo USB e drivers.")
    exit()

# Tenta conectar
while True:
    try:
        ser = serial.Serial(porta_arduino, 9600, timeout=1)
        print(f"Conectado com sucesso à porta {porta_arduino}!")
        break
    except serial.SerialException as e:
        print("Erro ao abrir porta:", e)
        print("Tentando novamente em 2 segundos...")
        time.sleep(2)

# Loop de leitura
print("Lendo dados do Arduino...\n")

while True:
    try:
        dado = ser.readline().decode(errors="ignore").strip()
        if dado:
            print("Recebido:", dado)
    except Exception as e:
        print("Erro na leitura:", e)
        break
