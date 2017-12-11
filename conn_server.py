import socket
import sys
import threading


def broadcastData(sock, message):
    for socket in CONNECTION_LIST:
        if socket != s and socket != sock:
            try :
                socket.send(message.encode('ascii'))
            except :
                socket.close()
                CONNECTION_LIST.remove(socket)

def escucharCliente(cliente, direccion):
    size=1024
    cliente.send('bienvenido al chat\n'.encode('ascii'))
    while True:
        data = cliente.recv(size).decode('ascii')
        print(data + ' de ' + direccion[0] + ':' + str(direccion[1]))
        if data:
            broadcastData(cliente, "\r" + '<' + str(cliente.getpeername()) + '> ' + data)
        '''
        if data: 
            cliente.send(('Recivido ' + data).encode('ascii'))
        else:
            raise error('cliente desconectado')
        '''


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
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        CONNECTION_LIST.append(conn)
        threads.append(threading.Thread(target = escucharCliente, args = (conn,addr, )).start())
        broadcastData(conn, "[%s:%s] entered room\n" % addr)
    
    s.close()
