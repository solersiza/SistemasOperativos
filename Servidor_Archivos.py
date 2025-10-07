import socket
import threading
import os

HOST = "192.168.1.21"  # Cambia por la IP del servidor
PORT = 5000
BUFFER_SIZE = 1024

# Carpeta donde se guardarán los archivos recibidos
CARPETA_DESTINO = "archivos_recibidos"
os.makedirs(CARPETA_DESTINO, exist_ok=True)

def manejar_cliente(conn, addr):
    try:
        print(f"[+] Conexión establecida con {addr}")

        # 🔹 Recibir nombre del archivo
        filename = conn.recv(BUFFER_SIZE).decode()
        if not filename:
            print(f"[-] Cliente {addr} no envió nombre de archivo.")
            conn.close()
            return

        # Responder ACK
        conn.sendall("OK".encode())

        # 🔹 Crear nombre de archivo con la IP del cliente
        ip_cliente = addr[0].replace(".", "_")  # Reemplaza puntos por guiones bajos
        nombre_guardado = f"recibido_{ip_cliente}_{filename}"
        filepath = os.path.join(CARPETA_DESTINO, nombre_guardado)

        # 🔹 Guardar el archivo
        with open(filepath, "wb") as f:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                f.write(data)

        print(f"[✔] Archivo '{filename}' recibido desde {addr} y guardado como '{nombre_guardado}'")

        # 🔹 Preguntar al cliente si quiere devolución
        conn.sendall("¿Quieres que te devuelva el archivo? (DEVOLVER/NO)".encode())

        respuesta = conn.recv(BUFFER_SIZE).decode().strip().upper()
        if respuesta == "DEVOLVER":
            print(f"[↩] Devolviendo archivo '{filename}' a {addr}")
            with open(filepath, "rb") as f:
                while chunk := f.read(BUFFER_SIZE):
                    conn.sendall(chunk)
            conn.shutdown(socket.SHUT_WR)
            print(f"[✔] Archivo '{filename}' devuelto a {addr}")
        else:
            print(f"[✖] Cliente {addr} no pidió devolución.")

    except Exception as e:
        print(f"[!] Error con {addr}: {e}")
    finally:
        conn.close()
        print(f"[x] Conexión cerrada con {addr}")


def servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[SERVIDOR] Esperando conexiones en {HOST}:{PORT}...")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=manejar_cliente, args=(conn, addr)).start()

if _name_ == "_main_":
    servidor()