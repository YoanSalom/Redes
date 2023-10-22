import socket
import json
import threading

# Configuración del servidor
host = '127.0.0.1'
port = 12345

# Crear un socket del servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlazar el socket al host y puerto
servidor.bind((host, port))

# Escuchar conexiones entrantes
servidor.listen()

print(f"Servidor escuchando en {host}:{port}")

# Lista para almacenar las conexiones de los clientes
clientes = []

# Función para manejar la comunicación con un cliente
def manejar_cliente(cliente_socket):
    while True:
        # Recibir datos del cliente
        datos = cliente_socket.recv(1024).decode()

        if not datos:
            break

        # Procesar los datos JSON recibidos
        datos_json = json.loads(datos)
        print(f"Datos recibidos desde {cliente_socket.getpeername()}: {datos_json}")

        # Enviar una respuesta
        respuesta = {"mensaje": "¡Datos recibidos con éxito!"}
        respuesta_json = json.dumps(respuesta)
        cliente_socket.send(respuesta_json.encode())

    # Cerrar la conexión
    cliente_socket.close()
    clientes.remove(cliente_socket)

# Ciclo principal del servidor
while True:
    # Aceptar una conexión entrante
    cliente_socket, cliente_direccion = servidor.accept()
    print(f"Conexión aceptada desde {cliente_direccion}")
    clientes.append(cliente_socket)

    # Iniciar un hilo para manejar la comunicación con el cliente
    cliente_thread = threading.Thread(target=manejar_cliente, args=(cliente_socket,))
    cliente_thread.start()