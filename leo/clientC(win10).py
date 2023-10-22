import socket
import json
import random
import threading
import queue
import time
import pygame
import sys

# ------- Funciones ------
def ui():
    global ejecutando
    global uitasks
    global uicoords
    global turno
    global user_hp
    global enemy_hp
    global own_ships
    global sfx
    try:
        # Inicializa Pygame
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("bmg.mp3")  # Cambia "tu_musica.mp3" por la ruta de tu archivo de música
        pygame.mixer.music.play(-1)  # -1 indica que la música se repetirá indefinidamente
        # Establece el volumen (0.0 a 1.0)
        pygame.mixer.music.set_volume(0.5)  # Ejemplo: volumen al 50%

        sfx_miss = pygame.mixer.Sound("miss.mp3")  # Cambia "tu_efecto_de_sonido.wav" por la ruta de tu archivo de sonido
        sfx_impact = pygame.mixer.Sound("impact.mp3")  # Cambia "tu_efecto_de_sonido.wav" por la ruta de tu archivo de sonido
        sfx_miss.set_volume(0.5)
    
        # Definir las dimensiones de la ventana
        ventana_ancho = 1280
        ventana_alto = 720

        # Definir el tamaño de los cuadrados y la cantidad de filas y columnas
        cuadro_lado = 100
        filas = 5
        columnas = 5

        # Crear una ventana
        ventana = pygame.display.set_mode((ventana_ancho, ventana_alto))
        # Cambia el título de la ventana
        pygame.display.set_caption("BattleShip - Leonardo Rodriguez")

        # Crear una segunda superficie para el segundo tablero
        segundo_tablero = pygame.Surface((cuadro_lado * columnas, cuadro_lado * filas))

        # Inicializa el reloj de Pygame
        reloj = pygame.time.Clock()



        # Variables para el tiempo de ejecución
        tiempo_inicial = pygame.time.get_ticks()  # Tiempo en milisegundos

        # Colores
        blanco = (255, 255, 255)
        negro = (0, 0, 0)
        rojo = (255, 0, 0)
        verde = (0, 255, 0)
        azul = (0,0,255)
        celeste = (135, 206, 235)
        gris = (128, 128, 128)
        numeros = ["0","1","2","3","4"]


        # Función para pintar un cuadro en un tablero
        def pintar_cuadro(tablero, x, y, color):
            tablero.fill(color, (x, y, cuadro_lado, cuadro_lado))
            pygame.draw.rect(tablero, negro, (x, y, cuadro_lado, cuadro_lado), 2)

        # Campos de entrada de texto
        campo1 = ""
        campo2 = ""

        # Fuentes
        fuente = pygame.font.Font(None, 36)

        # Rectángulos para los campos de entrada
        rectangulo_campo1 = pygame.Rect(0, 0, 300, 40)
        rectangulo_campo2 = pygame.Rect(300, 0, 300, 40)

        # Rectángulo para el botón
        rectangulo_boton = pygame.Rect(700, 0, 100, 40)

        # Variable global para el color del cuadrado
          # Inicialmente verdadero (verde)
        #ejecutando = True
        # Bucle principal

        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                elif evento.type == pygame.KEYDOWN:
                    if rectangulo_campo1.collidepoint(pygame.mouse.get_pos()):
                        if evento.key == pygame.K_BACKSPACE:
                            campo1 = campo1[:-1]
                        else:
                            campo1 += evento.unicode
                    elif rectangulo_campo2.collidepoint(pygame.mouse.get_pos()):
                        if evento.key == pygame.K_BACKSPACE:
                            campo2 = campo2[:-1]
                        else:
                            campo2 += evento.unicode
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    # Detectar clic en el botón
                    if rectangulo_boton.collidepoint(evento.pos):
                        
                        
                        # Cambiar el color del cuadrado
                        #turno = not turno # varible de control para enviar o no
                        if(turno):
                            #print("Contenido del campo 1:", campo1)
                            #print("Contenido del campo 2:", campo2)
                            uicoords.put([int(campo1),int(campo2)])
                            turno = not turno
                        # Limpiar los campos de entrada
                        campo1 = ""
                        campo2 = ""

            # Dibujar el fondo blanco
            ventana.fill(azul)
            segundo_tablero.fill(blanco)

            # Dibujar el primer tablero con la función
            for fila in range(filas):
                for columna in range(columnas):
                    x = 100 + columna * cuadro_lado
                    y = 100 + fila * cuadro_lado

                    # Llamamos a la función para pintar un cuadro en el primer tablero
                    pintar_cuadro(ventana, x, y, blanco)

            # Dibujar el segundo tablero con la función
            for fila in range(filas):
                for columna in range(columnas):
                    x = 700 + columna * cuadro_lado
                    y = 100 + fila * cuadro_lado

                    # Llamamos a la función para pintar un cuadro en el segundo tablero
                    pintar_cuadro(segundo_tablero, columna * cuadro_lado, fila * cuadro_lado, blanco)

            

            for i in range(len(own_ships)):
                pintar_cuadro(ventana, 100 + own_ships[i][0] * cuadro_lado, 100 + own_ships[i][1] * cuadro_lado,gris)

            if(len(uitasks)>0):
                for i in range(len(uitasks)):
                    if(uitasks[i][0] == "u"):
                        if(uitasks[i][1] == "i"):
                            
                            pintar_cuadro(ventana, 100 + uitasks[i][2] * cuadro_lado, 100 + uitasks[i][3] * cuadro_lado,rojo)
                        else:
                            pintar_cuadro(ventana, 100 + uitasks[i][2] * cuadro_lado, 100 + uitasks[i][3] * cuadro_lado,azul)
                    if(uitasks[i][0] == "e"):
                        if(uitasks[i][1] == "i"):
                            pintar_cuadro(segundo_tablero, 100 + uitasks[i][2] * cuadro_lado, 100 + uitasks[i][3] * cuadro_lado,rojo)
                        else:
                            pintar_cuadro(segundo_tablero, 100 + uitasks[i][2] * cuadro_lado, 100 + uitasks[i][3] * cuadro_lado,azul)
                        pass

            if(not sfx.empty()):
                info = sfx.get()
                if(info == "i"):
                    sfx_impact.play()
                if(info == "m"):
                    sfx_miss.play()
                #Llamamos a la función para pintar un cuadro en el primer tablero (por ejemplo, en la posición (1, 2) de la cuadrícula).
                #pintar_cuadro(ventana, 100 + 1 * cuadro_lado, 100 + 2 * cuadro_lado, rojo)
                #pintar_cuadro(ventana, 100 + 2 * cuadro_lado, 100 + 2 * cuadro_lado, rojo)
                # Llamamos a la función para pintar un cuadro en el segundo tablero en la posición (2, 2).
                #pintar_cuadro(segundo_tablero, 2 * cuadro_lado, 2 * cuadro_lado, rojo)

            # Dibujar el cuadrado que cambia de color en (1000, 0)
            pintar_cuadro(ventana, 0, 300, verde if turno else rojo)

            # Dibujar los campos de entrada de texto
            pygame.draw.rect(ventana, blanco, rectangulo_campo1, 2)
            pygame.draw.rect(ventana, blanco, rectangulo_campo2, 2)

            campo_superficie1 = fuente.render(campo1, True, blanco)
            campo_superficie2 = fuente.render(campo2, True, blanco)

            ventana.blit(campo_superficie1, (rectangulo_campo1.x + 5, rectangulo_campo1.y + 5))
            ventana.blit(campo_superficie2, (rectangulo_campo2.x + 5, rectangulo_campo2.y + 5))

            textU = f"Hp: {user_hp}"
            textE = f"Enemy Hp: {enemy_hp}"
            labelU = fuente.render(textU, True, blanco)
            labelE = fuente.render(textE, True, blanco)
            ventana.blit(labelU, (300,620))
            ventana.blit(labelE, (900,620))

            # Calcula el tiempo de ejecución en segundos
            tiempo_actual = pygame.time.get_ticks()  # Tiempo en milisegundos
            tiempo_transcurrido = (tiempo_actual - tiempo_inicial) // 1000  # Tiempo en segundos

            # Crea un "label" con el tiempo de ejecución
            texto_tiempo = f"Time: {tiempo_transcurrido} segundos"
            label_tiempo = fuente.render(texto_tiempo, True, blanco)
            ventana.blit(label_tiempo, (550,620))

            # Dibujar el botón
            pygame.draw.rect(ventana, negro, rectangulo_boton, 2)
            pygame.draw.rect(ventana, blanco, rectangulo_boton)

            texto_boton = fuente.render("atacar", True, negro)
            ventana.blit(texto_boton, (rectangulo_boton.x + 15, rectangulo_boton.y + 5))

            for i in range(len(numeros)):
                text_number = fuente.render(numeros[i], True, blanco)
                ventana.blit(text_number, (750 + 100*i, 70))
                ventana.blit(text_number, (670, 140 + 100*i))
            
            giveUp = "X     (Rendirse x = 9 | y = 9)        Y"
            gu = fuente.render(giveUp, True, blanco)
            ventana.blit(gu, (100, 50))

            # Actualizar la ventana
            ventana.blit(segundo_tablero, (700, 100))
            pygame.display.flip()

        # Salir de Pygame
        pygame.quit()
        sys.exit()
    except Exception as e:
        print(f"Error al recibir mensajes del servidor: {e}")

def rep_mov(lista_de_tuplas, tupla_a_buscar):
    return tupla_a_buscar in lista_de_tuplas

def esta_en_rango(x, y):
    return 0 <= x <= 4 and 0 <= y <= 4


def getFeedback(cola,accion):
    datos = cola.get()
    if(datos["status"] == 0 and datos["action"] == accion):
        return False
    elif(datos["status"] == 1 and datos["action"] == accion):
        return True
    else:
        return False

def sendMsj(msj):
    data["action"] = msj
    json_data = json.dumps(data)
    client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))

def colocar_caracter(tablero, x, y, caracter):
    # Verificar si las coordenadas están dentro del tablero
    if x < 0 or x >= 5 or y < 0 or y >= 5:
        print("Error: Coordenadas fuera del rango del tablero.")
        return
    # Colocar el carácter en la posición especificada
    tablero[y][x] = caracter

def imprimir_dos_tableros(tablero1, tablero2,user_hp,enemy_hp):
    print("\n")
    if len(tablero1) != 5 or len(tablero2) != 5:
        print("Error: Los tableros deben ser de tamaño 5x5.")
        return
    
    print("Tablero Usuario         Tablero Enemigo")
    print(f"hp: {user_hp}                   hp: {enemy_hp} \n")
    # Imprimir números en la parte superior
    print("    0 1 2 3 4               0 1 2 3 4")
    print("    _ _ _ _ _               _ _ _ _ _")
    
    for i in range(5):
        fila1 = " ".join(map(str, tablero1[i]))
        fila2 = " ".join(map(str, tablero2[i]))
        
        # Imprimir número a la izquierda
        print(f"{i} | {fila1}           {i} | {fila2}")

    print("\n")

def generate_tab(tablero):
    p = generar_barco_aleatorio()
    while(colocar_barco(p[0],p[1],p[2],tablero,1)== False):
        p = generar_barco_aleatorio()
    b = generar_barco_aleatorio()
    while(colocar_barco(b[0],b[1],b[2],tablero,2)== False):
        b = generar_barco_aleatorio()
    s = generar_barco_aleatorio()
    while(colocar_barco(s[0],s[1],s[2],tablero,3)== False):
        s = generar_barco_aleatorio()
    return [p,b,s]

def colocar_barco(x, y, direccion, tablero, largo):
    if x < 0 or x >= 5 or y < 0 or y >= 5:
        #print("Error: Coordenadas fuera del tablero.")
        return False
    if direccion == 0:  # Vertical
        if y + largo > 5:
            #print("Error: El barco no cabe en posición vertical.")
            return False
    elif direccion == 1:  # Horizontal
        if x + largo > 5:
            #print("Error: El barco no cabe en posición horizontal.")
            return False
    else:
        #print("Error: Dirección inválida.")
        return False
    # Verificar que no haya superposición con otros barcos
    if direccion == 0:  # Vertical
        for i in range(largo):
            if tablero[y + i][x] == 1:
                #print("Error: Superposición con otro barco.")
                return False
    elif direccion == 1:  # Horizontal
        for i in range(largo):
            if tablero[y][x + i] == 1:
                #print("Error: Superposición con otro barco.")
                return False

    # Colocar el barco en el tablero
    if direccion == 0:  # Vertical
        for i in range(largo):
            tablero[y + i][x] = 1
    elif direccion == 1:  # Horizontal
        for i in range(largo):
            tablero[y][x + i] = 1
    #print("Barco colocado con éxito.")
    return True

def generar_barco_aleatorio():
    x = random.randint(0, 4)  # Generar una coordenada x aleatoria entre 0 y 4 (inclusivo)
    y = random.randint(0, 4)  # Generar una coordenada y aleatoria entre 0 y 4 (inclusivo)
    orientacion = random.choice([0, 1])  # Elegir aleatoriamente entre 0 (vertical) y 1 (horizontal)
    return [x, y, orientacion]

def getMyships(tab):
    r = []
    for x in range(5):
        for y in range(5):
            if(tab[x][y] == 1):
                r.append((y,x))
    return r

def recibir_mensajes():
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            json_data = message.decode('utf-8')
            received_data = json.loads(json_data)
            colaMsj.put(received_data)
        except Exception as e:
            print(f"Error al recibir mensajes del servidor: {e}")
            break

#  ------Varibles-------
server_host = '172.20.60.123' 
server_port = 20001
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = {
    "action": "c, a, l, b, d, s",  # connection, attack, lose, build, disconnect, select
    "bot": 0,  # 0 o 1, 1: partida vs bot, 0: partida vs otro cliente

    "ships": {
        "p": [1, 2, 0],  # cordenada (x,y) y orientación (0: vertical, 1: horizontal)
        "b": [4, 1, 0],
        "s": [1, 2, 0]
    },
    "position": [3, 3],  # posicion de ataque
}

json_data = json.dumps(data)
colaMsj = queue.Queue()

user_hp = 6
tabUser = [[0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0]]

enemy_hp = 6
tabEnemy = [[0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0]]

# ---------- variables de control -------------

ini_demon = True
is_connected = False
has_gameMode = False
has_ships = False
can_attack = False
user_move_history = []
waiting_time = (random.randint(500, 5000))/1000
ejecutando = False
uitasks = [] # (tablero(ue),i-f,x,y) impacto fallo
uicoords = queue.Queue()# para enviar en main
turno = False
sfx = queue.Queue()
#tareas ["accion",x,y,color]
# --------- flujo principal --------------

data["action"] = "xx"
json_data = json.dumps(data)
client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))

while True:

    if ini_demon:# El hilo se ejecutará en segundo plano
        receiving_thread = threading.Thread(target=recibir_mensajes)
        receiving_thread.daemon = True  
        receiving_thread.start()
        ini_demon = False

    if not is_connected:
        data["action"] = "c"
        json_data = json.dumps(data)
        client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))
        #time.sleep(waiting_time)
        print("Esperando conexion con el servidor")
        while(colaMsj.empty()):
            print(".", end='', flush=True)
            time.sleep(waiting_time)
        if(getFeedback(colaMsj,"c")):
            print("conexion exitosa! \n")
            is_connected = True

    elif not has_gameMode and is_connected:
        data["action"] = "s"
        ch = input("1=bot | 0=player: ")
        while ch!= "1" and ch!= "0" :
            ch = input("1=bot | 0=player: ").lower()
        data["bot"] = ch
        if(ch == "1"):
            waiting_time = (random.randint(250, 1000))/1000
        json_data = json.dumps(data)
        client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))
        #time.sleep(waiting_time)
        print("Esperando por emparejamiento")
        while(colaMsj.empty()):
            print(".", end='', flush=True)
            time.sleep(waiting_time)
        if(getFeedback(colaMsj,"s")):
            if ch == "0":
                print("conexion a otro jugador")
                has_gameMode = True
            else:
                has_gameMode = True
                print("versus bot(server)")

    elif not has_ships and has_gameMode:
        data["action"] = "b"
        tablero = generate_tab(tabUser)
        data["ships"]["p"] = tablero[0]
        data["ships"]["b"] = tablero[1]
        data["ships"]["s"] = tablero[2]
        json_data = json.dumps(data)
        client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))
        #time.sleep(waiting_time)
        #print("Esperando respuesta del servidor")
        while(colaMsj.empty()):
            #print(".", end='', flush=True)
            time.sleep(waiting_time)
        if(getFeedback(colaMsj,"b")):
            #print("barcos puestos exitosamente!  \n")
            has_ships = True
            can_attack = True
            #imprimir_dos_tableros(tabUser,tabEnemy,user_hp,enemy_hp)
            own_ships = getMyships(tabUser)
            ejecutando = True
            ui_thread = threading.Thread(target=ui)
            ui_thread.daemon = True  
            ui_thread.start()
            

    elif user_hp == 0 or enemy_hp == 0:
        #preguntar si gane o perdi
        data["action"] = "w"
        json_data = json.dumps(data)
        client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))
        #time.sleep(waiting_time)
        print("Esperando resultado de la partida ")
        while(colaMsj.empty()):
            print(".", end='', flush=True)
            time.sleep(waiting_time)
        if(getFeedback(colaMsj,"w")):
            #gane
            print("ganaste!!!")
        else:
            #perdi
            print("perdiste")

        data["action"] = "d"
        json_data = json.dumps(data)
        client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))
        #time.sleep(waiting_time)
        print("Finalizando partida")
        ejecutando = False
        while(colaMsj.empty()):
            print(".", end='', flush=True)
            time.sleep(waiting_time)
        if(getFeedback(colaMsj,"d")):
            #desconexion del server
            print("fin del juego")
            break

        pass

    elif can_attack and (user_hp > 0 and enemy_hp > 0):
        #preguntar si mi mi turno
        data["action"] = "t"
        json_data = json.dumps(data)
        client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))
        #time.sleep(waiting_time)
        #print("Esperando respuesta del servidor")
        while(colaMsj.empty()):
            
            #print(".", end='', flush=True)
            time.sleep(waiting_time)

        if(getFeedback(colaMsj,"t")):
            turno = True
            #ataque
            #print("Tu turno!! (rendirse excribir x = 9 | y = 9)")
            
            while(uicoords.empty()):
                time.sleep(1)
            co = uicoords.get()
            x = co[0]
            y = co[1]
            if (x == 9 and y == 9):
                data["action"] = "l"
                user_hp = 0
                json_data = json.dumps(data)
                client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))
                #feedback falta
                pass
            else:
                data["action"] = "a"
                #while(not esta_en_rango(x,y) or (x,y)in user_move_history):
                    #print(f"coordenas ({x},{y}) ya jugadas o fuera del tablero!")
                    #x = int(input("X: "))
                    #y = int(input("Y: "))
                data["position"][0] = x
                data["position"][1] = y
                user_move_history.append((x,y))
                json_data = json.dumps(data)
                client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))
                #time.sleep(waiting_time)
                #print("Esperando resultado ataque")
                while(colaMsj.empty()):
                    # (tablero(ue),i-f,x,y) impacto fallo
                    #print(".", end='', flush=True)
                    time.sleep(waiting_time)
                if(getFeedback(colaMsj,"a")):
                    #acerte
                    #print("\n acierto!!")
                    colocar_caracter(tabEnemy,x,y,"X")
                    enemy_hp = enemy_hp - 1
                    #imprimir_dos_tableros(tabUser,tabEnemy,user_hp,enemy_hp)
                    uitasks.append(("e","i",x-1,y-1))
                    sfx.put("i")
                else:
                    #falle
                    #print("\nfallo!!")
                    colocar_caracter(tabEnemy,x,y,"Z")
                    #imprimir_dos_tableros(tabUser,tabEnemy,user_hp,enemy_hp)
                    uitasks.append(("e","f",x-1,y-1))
                    sfx.put("m")
                    pass
                        
        else:
            turno = False
            #esperar ataque
            #time.sleep(waiting_time)
            #print("Esperando ataque enemigo")
            while(colaMsj.empty()):
                #print(".", end='', flush=True)
                time.sleep(waiting_time)
            data = colaMsj.get()
            if(data["action"] == "a"):
                if(data["status"] == 1):
                    #print("te dieron!! \n")
                    user_hp = user_hp - 1
                    colocar_caracter(tabUser,data["position"][0],data["position"][1],"X")
                    #imprimir_dos_tableros(tabUser,tabEnemy,user_hp,enemy_hp)
                    uitasks.append(("u","i",data["position"][0],data["position"][1]))
                    sfx.put("i")
                    #me pego
                    pass
                else:
                    #fallo
                    #print("fallo!! \n")
                    colocar_caracter(tabUser,data["position"][0],data["position"][1],"Z")
                    #imprimir_dos_tableros(tabUser,tabEnemy,user_hp,enemy_hp)
                    uitasks.append(("u","f",data["position"][0],data["position"][1]))
                    sfx.put("m")
                    pass
            if(data["action"] == "l"):
                if(data["status"] == 1):
                    print("enemigo se rindio! jajsdj xd")
                    enemy_hp = 0
                    #imprimir_dos_tableros(tabUser,tabEnemy,user_hp,enemy_hp)
                pass
    
# Cerrar el socket al finalizar
client_socket.close()