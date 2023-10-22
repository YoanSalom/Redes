import socket
import json
import random
import threading  # Importa el módulo threading para trabajar con hilos

hp_lock = threading.Lock()
hp = 6

def sendMsj(msj,val):
    print("Perdiste Bro :c")
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

def imprimir_dos_tableros(tablero1, tablero2):
    print("\n")
    if len(tablero1) != 5 or len(tablero2) != 5:
        print("Error: Los tableros deben ser de tamaño 5x5.")
        return
    
    print("Tablero Usuario         Tablero Enemigo \n")
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
    # Verificar que las coordenadas estén dentro del tablero (5x5)
    if x < 0 or x >= 5 or y < 0 or y >= 5:
        #print("Error: Coordenadas fuera del tablero.")
        return False

    # Verificar que las coordenadas iniciales sean válidas
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

# Función para manejar la recepción de mensajes del servidor
def recibir_mensajes():
    global hp
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            json_data = message.decode('utf-8')
            received_data = json.loads(json_data)
            print(f"\n Mensaje del servidor: {message.decode('utf-8')} \n")
            if(received_data["action"]=="a" and received_data["status"] == 1):
                print("acierto")
                colocar_caracter(tabEnemy,received_data["position"][0],received_data["position"][1],"X")
                imprimir_dos_tableros(tabUser,tabEnemy)
                #hp = hp - 1
            if(received_data["action"]=="a" and received_data["status"] == 0):
                print("fallo")
                colocar_caracter(tabEnemy,received_data["position"][0],received_data["position"][1],"Z")
                imprimir_dos_tableros(tabUser,tabEnemy)
            if(received_data["action"]=="s" and received_data["status"] == 1):
                with hp_lock:
                    hp = hp - 1
                
                print("hp:")
                print(hp)
                if hp == 0:
                    sendMsj("l",1)
                colocar_caracter(tabUser,received_data["position"][0],received_data["position"][1],"X")
                imprimir_dos_tableros(tabUser,tabEnemy)


            if(received_data["action"]=="s" and received_data["status"] == 0):
                colocar_caracter(tabUser,received_data["position"][0],received_data["position"][1],"Z")
                imprimir_dos_tableros(tabUser,tabEnemy)

            if(received_data["action"]=="l" and received_data["status"] == 1):
                print("\n ganaste bro!! \n")
            
        except Exception as e:
            print(f"Error al recibir mensajes del servidor: {e}")
            break

# Configuración del cliente
#server_host = '127.0.0.1'  # Dirección IP del servidor
server_host = '172.20.60.123' 

server_port = 12346      # Puerto del servidor

# Crear un socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Crear un diccionario JSON
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
frun = True


enemy_hp = 6

tabUser = [[0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0]]

tabEnemy = [[0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0]]

while True:    

            

    accion = input("c|b|a: ").lower()
    
    if accion.lower() == 'exit':
        break
    
    elif accion == "c":
        data["action"] = "c"
        ch = input("1=bot | 0=player: ").lower()
        data["bot"] = ch
        pass
    elif accion == "b":
        data["action"] = "b"
        tablero = generate_tab(tabUser)
        data["ships"]["p"] = tablero[0]
        data["ships"]["b"] = tablero[1]
        data["ships"]["s"] = tablero[2]
        imprimir_dos_tableros(tabUser,tabEnemy)
        
    elif accion == "a":
        data["action"] = "a"
        x = int(input("X: "))
        y = int(input("Y: "))
        data["position"][0] = x
        data["position"][1] = y
        pass
    
    elif accion == "l":
        data["action"] = "l"

    else:
        pass
    
    json_data = json.dumps(data)

    # Enviar el mensaje al servidor
    client_socket.sendto(json_data.encode('utf-8'), (server_host, server_port))

    if frun:
        receiving_thread = threading.Thread(target=recibir_mensajes)
        receiving_thread.daemon = True  # El hilo se ejecutará en segundo plano
        receiving_thread.start()
        frun = False
    
# Cerrar el socket al finalizar
client_socket.close()
