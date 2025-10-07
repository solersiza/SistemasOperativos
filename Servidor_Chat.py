import socket
import threading

HOST = "192.168.1.21"  # IP del servidor 
PORT = 5000
BUFFER_SIZE = 1024

clientes = []  # Lista de conexiones activas
nombres = {}   # Diccionario {conn: nombre}

def broadcast(mensaje, remitente=None):
    """Envía el mensaje a todos los clientes excepto al remitente."""
    for cliente in clientes:
        if cliente != remitente:
            try:
                cliente.sendall(mensaje.encode())
            except:
                cliente.close()
                if cliente in clientes:
                    clientes.remove(cliente)

def manejar_cliente(conn, addr):
    print(f"[+] Nueva conexión desde {addr}")

    # Pedir nombre al cliente
    conn.sendall("Escribe tu nombre: ".encode())
    nombre = conn.recv(BUFFER_SIZE).decode().strip()
    nombres[conn] = nombre

    bienvenida = f"👋 {nombre} se ha unido al chat."
    print(bienvenida)
    broadcast(bienvenida, remitente=conn)

    try:
        while True:
            msg = conn.recv(BUFFER_SIZE).decode()
            if not msg:
                break

            if msg.lower() == "/salir":
                conn.sendall("Desconectándote del chat...".encode())
                break

            mensaje_formateado = f"[{nombre}]: {msg}"
            print(mensaje_formateado)
            broadcast(mensaje_formateado, remitente=conn)

    except Exception as e:
        print(f"[!] Error con {addr}: {e}")

    finally:
        print(f"[x] {nombre} ({addr}) se desconectó.")
        conn.close()
        clientes.remove(conn)
        broadcast(f"❌ {nombre} salió del chat.")
        del nombres[conn]

def servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[SERVIDOR] Esperando conexiones en {HOST}:{PORT}...")

        while True:
            conn, addr = s.accept()
            clientes.append(conn)
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
            hilo.start()

if __name__ == "__main__":
    servidor()
