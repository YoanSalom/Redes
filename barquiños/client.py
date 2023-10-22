import pygame
import socket
import json

# Configuración del cliente
host = '127.0.0.1'
port = 12345

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Cliente Pygame")

# Crear un socket del cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
cliente.connect((host, port))

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Crear un diccionario de datos
    datos = {
        "jugador": "Jugador 1",
        "puntos": 100,
        "nivel": 5
    }

    # Convertir el diccionario a JSON y enviarlo al servidor
    datos_json = json.dumps(datos)
    cliente.send(datos_json.encode())

    # Recibir la respuesta del servidor
    respuesta = cliente.recv(1024).decode()
    respuesta_json = json.loads(respuesta)
    print("Respuesta del servidor:", respuesta_json)

    pantalla.fill((0, 0, 0))
    pygame.display.update()