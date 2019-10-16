######################################################################################
# Instituto Tecnológico de Colima - División de Estudios de Posgrado e Investigación #
# Maestría en Sistemas Computacionales - Materia: Tecnologías de Internet            #
#                                                                                    #
# Código Fuente para Servidor UDP                                                    #
# Realizado por:                                                                     #
# Osvaldo Vladimir Rodríguez Leal                                                    #
# José Alfredo Cortés Quiroz                                                         #
# Villa de Álvarez, Col 16/10/19                                                     #
######################################################################################
from tkinter import *
from tkinter import scrolledtext
import socket
import threading

serverAddressPort = ("0.0.0.0", 20001)
bufferSize = 1024  

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
 
window = Tk() 
window.title("..::Cliente Chat UDP::..") 
window.geometry('380x440')  
area_conversation = scrolledtext.ScrolledText(window,width=45,height=20)
area_conversation.grid(column=1, row=0)

txt_in = Entry(window,width=15)
txt_in.grid(column=1, row=3)
txt_in.focus()

def clicked():
    res = "-->You: " + txt_in.get() + "\n"
    area_conversation.insert(INSERT, res)
    bytesToSend = str.encode(txt_in.get())  # codificamos la cadena a bytes
    UDPClientSocket.sendto(bytesToSend, serverAddressPort) # enviamos el texto al servidor    

def enter_key(Event):
    clicked()
txt_in.bind("<Return>", enter_key)
    
def data_recibe():
    while True:
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)  # asignamos el texto recibido  a una variable
        msg = "-->Server: {}".format(msgFromServer[0]) # añadimos texto y decodificamos el mensaje
        area_conversation.insert(INSERT, msg + "\n")
        
btn = Button(window, text="Send", bg="blue", fg="white", command=clicked)
btn.grid(column=1, row=4)

tread = threading.Thread(target = data_recibe)
tread.start()

window.mainloop()

