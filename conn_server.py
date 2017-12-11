import socket
import sys
import threading
import select


def broadcast_data(sock, message):
    for socket in CONNECTION_LIST:
        if socket != s and socket != sock:
            try :
                socket.send(message.encode('ascii'))
            except :
                socket.close()
                CONNECTION_LIST.remove(socket)


def escucharCliente(cliente, direccion):
    size=1024
    cliente.send('Bienvenido al Chat\n'.encode('ascii'))
    while True:
        data = cliente.recv(size).decode('ascii')
        print(data + ' de ' + direccion[0] + ':' + str(direccion[1]))
        if data:
            broadcast_data(cliente, "\r" + '<' + str(cliente.getpeername()) + '> ' + data)


if __name__ == "__main__":

    HOST = ''   # Symbolic name, meaning all available interfaces
    PORT = 8889 # Arbitrary non-privileged port
    CONNECTION_LIST = []

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

    #now keep talking with the client
    while 1:
        read_sockets,ws,es = select.select(CONNECTION_LIST,[],[])
        for sock in read_sockets:
            if sock == s:
                conn, addr = s.accept()
                CONNECTION_LIST.append(conn)
                threads.append(threading.Thread(target = escucharCliente, args = (conn,addr, )).start())
                broadcast_data(conn, "[%s:%s] entered room\n" % addr)
    
    s.close()
