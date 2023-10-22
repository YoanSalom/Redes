matriz = [[0] * 5 for _ in range(5)]
# Función para verificar si un barco puede ser colocado en la matriz
def validar_colocacion(matriz, barco, x, y):
    tipo = barco["tipo"]
    orientacion = barco["orientacion"]

    # Verificar si el barco cabe en la matriz en la orientación deseada
    if orientacion == "horizontal" and y + tipo > 5:
        return False
    if orientacion == "vertical" and x + tipo > 5:
        return False

    # Verificar si el barco se superpone con otros barcos
    for i in range(tipo):
        if orientacion == "horizontal" and matriz[x][y + i] != 0:
            return False
        if orientacion == "vertical" and matriz[x + i][y] != 0:
            return False

    return True

# Función para colocar un barco en la matriz
def colocar_barco(matriz, barco, x, y):
    tipo = barco["tipo"]
    orientacion = barco["orientacion"]

    for i in range(tipo):
        if orientacion == "horizontal":
            matriz[x][y + i] = tipo
        else:
            matriz[x + i][y] = tipo

# Ejemplo de colocación de un barco en la matriz
barco = {
    "barco1": {
        "tipo": 1,  # Barco de 1 celda
        "posicion": [(0, 0)],  # Coordenadas de las celdas ocupadas por el barco
        "orientacion": "horizontal"  # Puede ser "horizontal" o "vertical"
    },
    "barco2": {
        "tipo": 2,  # Barco de 2 celdas
        "posicion": [(1, 1), (1, 2)],  # Coordenadas de las celdas ocupadas por el barco
        "orientacion": "horizontal"
    },
    # Agregar más barcos según necesites
}


x = 1
y = 2

if validar_colocacion(matriz, barco, x, y):
    colocar_barco(matriz, barco, x, y)
    print("Barco colocado exitosamente")
else:
    print("No se puede colocar el barco en esa posición")

# Imprimir la matriz resultante
for fila in matriz:
    print(fila)