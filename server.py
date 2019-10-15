import socket
from threading import Thread


def accept_incoming_connections():
    #
    while True:
        client, client_address = SERVER.recvfrom(1024)
        #client, client_address = SERVER.accept()
        print("%s:%s Cliente conectado." % client_address)
        vaaars = 'Escribe tu nombre' 
        
        bytesAddressPair = SERVER.recvfrom(1024) # Devuelve un objeto de bytes leído por UDP y la dirección del socket del cliente
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        print(bytesAddressPair)
        clientMsg = "--> Client Say: {}".format(message)
        clientIP  = "MSG FROM IP: {}".format(address)    
        print(clientMsg) #imprimimos en pantalla el mensaje
        print(clientIP) # imprimimos en pantalla la dirección IP de donde se envia el mensaje
        msgFromServer = "--> You Say: " # asignamos el texto a enviar en una variable  
        bytesToSend = str.encode(msgFromServer) # Convertimos  a bytes para el envío
        SERVER.sendto(bytesToSend, clientIP) # Enviamos mensaje a cliente

        addresses[clientIP] = client_address
        Thread(target=saludo_mano, args=(client,)).start()


def saludo_mano():  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Bienvenido %s! Siquieres cerrar el chat escribe, ->   {quit} <- para salir.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s a entrado al chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s a dejado el chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

     #se definen los parametros que se utilizaran para abrir el socket, ip y puerto asi como el tamaño del buz de datos   
clients = {}
addresses = {}

HOST = "127.0.0.1"
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
#se inicializa el servidor por medio del socket como stream data
SERVER = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
#se hace el enlace con la direccion y puerto
SERVER.bind(ADDR)
#el servidor se mantiene a la escucha de algun cliente por medio del enlace previamente creado
if __name__ == "__main__":
   print("Eserando conexion de clientes...")
   accept_incoming_connections()