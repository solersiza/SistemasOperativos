import socket
from tkinter import Tk, filedialog
import os

HOST = "192.168.1.24"  # IP del servidor
PORT = 5000
BUFFER_SIZE = 1024

# Selección de archivo con ventana
Tk().withdraw()
filepath = filedialog.askopenfilename(title="Selecciona un archivo para enviar")

if not filepath:
    print("No seleccionaste ningún archivo.")
    exit()

filename = os.path.basename(filepath)

# 🔹 Preguntar antes si quiere devolución
opcion = input("¿Quieres que el servidor te devuelva el archivo? (DEVOLVER/NO): ").strip().upper()
if opcion not in ["DEVOLVER", "NO"]:
    print("Opción inválida, elige DEVOLVER o NO.")
    exit()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # Enviar primero la opción
    s.send(opcion.encode())

    # Enviar nombre del archivo
    s.send(filename.encode())

    # Esperar ACK
    ack = s.recv(BUFFER_SIZE).decode()
    if ack != "OK":
        print("Servidor no aceptó el archivo.")
        exit()

    # 🔹 Enviar archivo
    with open(filepath, "rb") as f:
        while chunk := f.read(BUFFER_SIZE):
            s.sendall(chunk)

    s.shutdown(socket.SHUT_WR)

    # 🔹 Si pidió devolución, recibirlo
    if opcion == "DEVOLVER":
        with open(f"devolucion_{filename}", "wb") as f:
            while True:
                data = s.recv(BUFFER_SIZE)
                if not data:
                    break
                f.write(data)
        print(f"[✔] Archivo '{filename}' recibido de vuelta.")

print(f"[✔] Archivo '{filename}' enviado correctamente.")

