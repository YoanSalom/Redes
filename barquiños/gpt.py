def verificar_matriz(matriz, longitud_minima, secuencias_de_2):
    def verificar_fila(fila, longitud_minima, secuencias_de_2):
        conteo = 0
        max_conteo = 0
        secuencias_2 = 0

        for elemento in fila:
            if elemento == 1:
                conteo += 1
                max_conteo = max(max_conteo, conteo)
                if max_conteo >= longitud_minima:
                    conteo = 0
            else:
                conteo = 0

            if elemento == 1 and max_conteo == 1:
                secuencias_2 += 1

        return max_conteo >= longitud_minima and secuencias_2 == secuencias_de_2

    def contar_secuencias(matriz, longitud_minima, secuencias_de_2):
        secuencias = 0
        secuencias_2 = 0

        for fila in matriz:
            secuencias += verificar_fila(fila, longitud_minima, secuencias_de_2)

        matriz_traspuesta = list(map(list, zip(*matriz)))
        for columna in matriz_traspuesta:
            secuencias += verificar_fila(columna, longitud_minima, secuencias_de_2)
            secuencias_2 += verificar_fila(columna, 1, secuencias_de_2)

        return secuencias, secuencias_2

    total_1s = sum(fila.count(1) for fila in matriz)

    secuencias_3, secuencias_2 = contar_secuencias(matriz, longitud_minima, secuencias_de_2)

    if total_1s == 6 and secuencias_3 == 1 and secuencias_2 == 1:
        return True

    return False

# Ejemplo de matriz
matriz = [
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [0, 0, 1, 0, 1]
]

longitud_minima = 3
secuencias_de_2 = 1

resultado = verificar_matriz(matriz, longitud_minima, secuencias_de_2)

if resultado:
    print(f"La matriz cumple con los criterios: tiene una única secuencia de {longitud_minima} o más unos consecutivos, dos secuencias de 2 unos, y el total de unos es igual a 6.")
else:
    print("La matriz no cumple con los criterios deseados.")