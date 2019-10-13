######################################################################################
# Instituto Tecnológico de Colima - División de Estudios de Posgrado e Investigación #
# Maestría en Sistemas Computacionales - Materia: Tecnologías de Internet            #
#                                                                                    #
# Código Fuente para Cliente Multicast UDP con interfas grafica usando Tkinter       #
# Realizado por:                                                                     #
# Osvaldo Vladimir Rodríguez Leal                                                    #
# José Alfredo Cortés Quiroz                                                         #
# Villa de Álvarez, Col 13/10/19                                                     #
######################################################################################
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    #intserta el mensaje a la lista de mensajes, y percibe si no ha salido el usuario 
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode('utf8')
            msg_list.insert(tkinter.END, msg)
        except OSError:  # cliente deja la sala o el canal
            break


def enviar(event=None):  
    msg = my_msg.get()
    my_msg.set("")  # despues de recoger el mensaje limpia el input del chat
    client_socket.send(bytes(msg, 'utf8'))#envia mensaje al servidor 
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    #cuando clikean en la X de salir se ponen en el chat el comando para quitarlo o cerrarlo
    my_msg.set("{quit}")
    send()

top = tkinter.Tk()
top.title("Chat multi cast")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # variable para los mensajes que escriba el usuario
my_msg.set("Escribe tus mensajes aqui.")
scrollbar = tkinter.Scrollbar(messages_frame)  # scroll en caso de que los mensajes sean muchos sale
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", enviar)
entry_field.pack()
#al presionar el boton enviar se mandan los parametros a enviar, funcion para enviar mensajes al server
send_button = tkinter.Button(top, text="Enviar", command=enviar)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#elementos para crear el scoket
HOST = '127.0.0.1'
PORT = 33000


BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()