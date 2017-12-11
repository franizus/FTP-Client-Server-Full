import socket
import sys
import threading
import select


def broadcast_data(client, message):
    for key in CONNECTION_DICT:
        sock = CONNECTION_DICT.get(key)
        if sock != s and sock != CONNECTION_DICT.get(client):
            sock.send(message.encode('ascii'))


def broadcast_connected_clients(socket):
    for key in CONNECTION_DICT:
        sock = CONNECTION_DICT.get(key)
        if sock != s and sock != CONNECTION_DICT.get(client):
            socket.send(('\r' + key + ' se encuentra en el chat\n').encode('ascii'))


def send_data(sender, receiver, message):
    if receiver in CONNECTION_DICT:
        sock = CONNECTION_DICT.get(receiver)
        if sock != s and sock != CONNECTION_DICT.get(client):
            sock.send(message.encode('ascii'))
    else:
        sock = CONNECTION_DICT.get(sender)
        sock.send((receiver + ' no conectado.\n').encode('ascii'))


def listen_client(client, socket, direccion):
    size=1024
    socket.send(('Bienvenido al Chat ' + client + '\n').encode('ascii'))
    broadcast_connected_clients(socket)
    while True:
        data = socket.recv(size).decode('ascii')
        if data:
            broadcast_data(client, '\r<' + client + '> ' + data)


if __name__ == "__main__":

    HOST = ''   # Symbolic name, meaning all available interfaces
    PORT = 8889 # Arbitrary non-privileged port
    CONNECTION_LIST = []
    CONNECTION_DICT = {}
    CLIENT_COUNTER = 0

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    
    threads = []
    #Start listening on socket
    s.listen(10)
    CONNECTION_LIST.append(s)
    CONNECTION_DICT.update({'Server':s})

    #now keep talking with the client
    while 1:
        read_sockets,ws,es = select.select(CONNECTION_LIST, [], [])
        for sock in read_sockets:
            if sock == s:
                conn, addr = s.accept()
                client = 'C' + str(CLIENT_COUNTER + 1)
                CONNECTION_LIST.append(conn)
                CONNECTION_DICT.update({client:conn})
                threads.append(threading.Thread(target = listen_client, args = (client, conn, addr, )).start())
                broadcast_data(client, '\r' + client + ' entro al chat\n')
                CLIENT_COUNTER += 1
    
    s.close()
