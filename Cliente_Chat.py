import socket
import threading
import sys

HOST = "192.168.1.21"  # IP del servidor
PORT = 5000
BUFFER_SIZE = 1024

def escuchar_servidor(sock):
    """Hilo que escucha los mensajes del servidor y los muestra."""
    while True:
        try:
            data = sock.recv(BUFFER_SIZE).decode()
            if not data:
                print("[!] Desconectado del servidor.")
                break
            print(data)
        except:
            print("[!] Error en la conexión.")
            sock.close()
            break

def cliente():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f"[+] Conectado al servidor {HOST}:{PORT}")
        except:
            print("[x] No se pudo conectar al servidor.")
            sys.exit()

        # Escuchar mensajes del servidor en hilo separado
        threading.Thread(target=escuchar_servidor, args=(s,), daemon=True).start()

        # Bucle de envío de mensajes
        while True:
            mensaje = input("")
            if mensaje.lower() == "/salir":
                s.sendall(mensaje.encode())
                print("[x] Saliendo del chat...")
                break
            try:
                s.sendall(mensaje.encode())
            except:
                print("[!] No se pudo enviar el mensaje.")
                break

if __name__ == "__main__":
    cliente()
