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
import queue

localIP = "0.0.0.0" # dirección ip local
localPort = 20001 # puerto de escucha
bufferSize = 1024 # tamaño del bufer

# La siguiente instrucción crea el Datagrama para UDP
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# La siguiente instrucción crea el servidor UDPP
UDPServerSocket.bind((localIP, localPort))

window = Tk() 
window.title("..::Servidor Chat UDP::..") 
window.geometry('380x430')  
area_conversation = scrolledtext.ScrolledText(window,width=45,height=20)
area_conversation.grid(column=1, row=0)
area_conversation.insert(INSERT, "..::Chat UDP Online::.."+ "\n")

txt_in = Entry(window,width=15)
txt_in.grid(column=1, row=3)
txt_in.focus()

def data_recibe():
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize) # Devuelve un objeto de bytes leído por UDP y la dirección del socket del cliente
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]        
        clientIP  = format(address)    
        clientMsg = format(message)
        area_conversation.insert(INSERT,clientIP +" Say: "+ clientMsg+ "\n")
        q.put(bytesAddressPair)
        

def clicked():
    client_IP= q.get()
    res = "-->You: " + txt_in.get() + "\n" 
    address = client_IP[1]
    area_conversation.insert(INSERT, res)
    bytesToSend = str.encode(txt_in.get()) # Convertimos  a bytes para el envío
    UDPServerSocket.sendto(bytesToSend,address) 

q = queue.Queue()

tread1 = threading.Thread(target = data_recibe)
tread2 = threading.Thread(target = clicked, args=q)

tread1.start()
tread2.start()

        
btn = Button(window, text="Send", bg="blue", fg="white", command=clicked)
btn.grid(column=1, row=4)

window.mainloop()

    