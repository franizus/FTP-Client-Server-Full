import socket
import sys
import threading


def receiveData(cliente, idc, lista):
    size = 1024
    while True:
        data = cliente.recv(size).decode('ascii')
        if data:
            lista[idc].append(data)


def sendData(cliente, idc, lista):
    while True:
        for i in range(len(lista)):
            if i != idc:
                if len(lista[i]) > 0:
                    cliente.send(lista[i][-1].encode('ascii'))


def escucharCliente(cliente, idc, lista):
    cliente.send('bienvenido al chat\n'.encode('ascii'))
    threading.Thread(target = receiveData, args = (cliente, idc, lista, )).start()
    threading.Thread(target = sendData, args = (cliente, idc, lista, )).start()


if __name__ == "__main__":

    HOST = ''   # Symbolic name, meaning all available interfaces
    PORT = 8888 # Arbitrary non-privileged port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    
    threads = []
    message_list = []
    #Start listening on socket
    s.listen(10) 

    #now keep talking with the client
    client_id = 0
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        message_list.append([])
        threads.append(threading.Thread(target = escucharCliente, args = (conn, client_id, message_list, )).start())
        client_id += 1
    
    s.close()
