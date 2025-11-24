import serial
import time

# Cambia COM3 por el puerto correcto si es necesario
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

print("=== CALIBRADOR DE SERVOS (PYTHON) ===")
print("Comandos:")
print(" i 0-180  -> índice")
print(" m 0-180  -> medio")
print(" a 0-180  -> anular + meñique")
print(" f 0-180  -> pulgar flexión")
print(" g 0-180  -> pulgar giro")
print("Ejemplo: i 90")
print("Escribe 'exit' para salir.\n")

while True:
    cmd = input("> ")

    if cmd.lower() == "exit":
        break

    try:
        letra, angulo = cmd.split()
        angulo = int(angulo)

        # Validación de seguridad
        if angulo < 0: angulo = 0
        if angulo > 180: angulo = 180

        # Convertimos a la forma del Arduino: a,b,c,d,e
        # Pero solo modificamos 1 servo a la vez.
        # Enviamos algo como: "i 90\n"
        mensaje = f"{letra} {angulo}\n"
        arduino.write(mensaje.encode())
        print(f"Enviado: {mensaje.strip()}")

    except:
        print("Formato incorrecto. Usa por ejemplo:  m 120  ó  f 60")

arduino.close()
