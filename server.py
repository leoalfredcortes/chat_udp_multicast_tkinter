######################################################################################
# Instituto Tecnológico de Colima - División de Estudios de Posgrado e Investigación #
# Maestría en Sistemas Computacionales - Materia: Tecnologías de Internet            #
#                                                                                    #
# Código Fuente para Servidor Multicast UDP                                          #
# Realizado por:                                                                     #
# Osvaldo Vladimir Rodríguez Leal                                                    #
# José Alfredo Cortés Quiroz                                                         #
# Villa de Álvarez, Col 13/10/19                                                     #
######################################################################################
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    #
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s Cliente conectado." % client_address)
        client.send(bytes("Escribe tu nickname y enviar o enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=saludo_mano, args=(client,)).start()


def saludo_mano(client):  # Takes client socket as argument.
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

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
#se inicializa el servidor por medio del socket como stream data
SERVER = socket(AF_INET, SOCK_STREAM)
#se hace el enlace con la direccion y puerto
SERVER.bind(ADDR)
#el servidor se mantiene a la escucha de algun cliente por medio del enlace previamente creado
if __name__ == "__main__":
    SERVER.listen(5)
    print("Eserando conexion de clientes...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()