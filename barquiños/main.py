import pygame
import sys


# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ventana = pygame.display.set_mode((1024, 700))
pygame.display.set_caption("BattleShip Yaxel")
reloj = pygame.time.Clock()

# Colores
morado = (150, 0, 150)
blanco = (255, 255, 255)
negro = (0,0,0)
rojo = (255,0,0)
azul = (0,255,255)
amarillo = (255, 128, 0)
verde = (0,255,0)

# Fuente
font = pygame.font.Font(None, 36)


# Variables para almacenar la elección del jugador
modo_seleccionado = None

#vida de jugador 1
vida_barco1 = 1
vida_barco2 = 2
vida_barco3 = 3

#vida de jugador 2
vida_barco4 = 1
vida_barco5 = 2
vida_barco6 = 3

# Tamaño de la matriz
filas = 5
columnas = 5

#grosor de cada ranura?
grosor_borde = 2

# Tamaño de cada celda
ancho_celda = 50
alto_celda = 50
#posicion inicial 
x = 50
y = 50
z = 720

# Matriz Usuario
matriz1 = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]
# Matriz Enemigo
matriz2= [
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1]
]



# Bucle principal
def main():
    ejecutando = True
    while ejecutando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Obtener las coordenadas del clic del mouse
                i, j = pygame.mouse.get_pos()
                
                # Calcular la fila y columna de la celda clickeada
                fila = (j - y) // alto_celda
                columna = (i - x) // ancho_celda

                # Cambiar el color de la celda clickeada
                if 0 <= fila < filas and 0 <= columna < columnas:
                    matriz1[fila][columna] = 1 - matriz1[fila][columna]  # Cambia entre 0 y 1
                    matriz2[fila][columna] = 1 - matriz2[fila][columna]

        # Limpiar la pantalla
        ventana.fill(morado)

        # Dibujar la matriz usuario   (ventana,color,(posicion(x,y),tamaño(x,y))
        pygame.draw.rect(ventana, amarillo, (0,0,550,2000))
        dibujar_barra_de_vida(ventana, 50, 100, vida_barco1, "Patrullero")
        dibujar_barra_de_vida(ventana, 50, 200, vida_barco2, "Barco")
        dibujar_barra_de_vida(ventana, 50, 300, vida_barco3, "Submarino")

        dibujar_barra_de_vida(ventana, 650, 100, vida_barco4, "Patrullero")
        dibujar_barra_de_vida(ventana, 650, 200, vida_barco5, "Barco")
        dibujar_barra_de_vida(ventana, 650, 300, vida_barco6, "Submarino")

        for fila in range(filas):
            for columna in range(columnas):
                if matriz1[fila][columna] == 0:
                                celda_rect = pygame.Rect(
                                x + columna * ancho_celda,
                                y + fila * alto_celda,
                        ancho_celda,
                        alto_celda
                    )
                                
                
                #matriz de color con su marco
                pygame.draw.rect(ventana, rojo, (x+columna * ancho_celda, y+fila * alto_celda, ancho_celda, alto_celda))
                pygame.draw.rect(ventana, azul, celda_rect)
                pygame.draw.rect(ventana, negro, celda_rect, grosor_borde)
                pygame.draw.rect(ventana, negro, (x+columna * ancho_celda, y+fila * alto_celda, ancho_celda, alto_celda), grosor_borde)
        
        for fila in range(filas):
            for columna in range(columnas):
                if matriz2[fila][columna] == 1:
                                celda_rect2 = pygame.Rect(
                                z + columna * ancho_celda,
                                y + fila * alto_celda,
                        ancho_celda,
                        alto_celda
                    )
                #matriz de color con su marco
                pygame.draw.rect(ventana, azul, (z + columna * ancho_celda, y+fila * alto_celda, ancho_celda, alto_celda))
                pygame.draw.rect(ventana, rojo, celda_rect2)
                pygame.draw.rect(ventana, negro, celda_rect2, grosor_borde)
                pygame.draw.rect(ventana, negro, (z + columna * ancho_celda, y+fila * alto_celda, ancho_celda, alto_celda), grosor_borde)
        
        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(60)

    # Salir del juego
    pygame.quit()
    sys.exit()

def dibujar_barra_de_vida(ventana, x, y, vida, nombre):
    longitud_total = 200
    longitud_actual = (vida / 3) * longitud_total
    borde_rect = pygame.Rect(x, y + 300 , longitud_total, 30)
    vida_rect = pygame.Rect(x, y + 300, longitud_actual, 30)

    pygame.draw.rect(ventana, blanco, borde_rect)
    pygame.draw.rect(ventana, verde, vida_rect)

    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(f"{nombre}", True, rojo)
    ventana.blit(texto, (x + longitud_total + 10, y + 300))    

if __name__ == "__main__":
    main()



