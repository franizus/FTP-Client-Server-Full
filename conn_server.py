""" Concurrent Chat Server module """
import socket
import sys
import threading
import select


def broadcast_data(client_id, message):
    """Broadcast a message to all the connected clients."""
    for key in CONNECTION_DICT:
        sock = CONNECTION_DICT.get(key)
        if sock != SERVER_SOCKET and sock != CONNECTION_DICT.get(client_id):
            sock.send(message.encode('ascii'))


def send_connected_clients(client_socket):
    """Sends the list of connected clients to the last client to connect."""
    for key in CONNECTION_DICT:
        sock = CONNECTION_DICT.get(key)
        if sock != SERVER_SOCKET and sock != CONNECTION_DICT.get(client):
            client_socket.send(
                ('\r' + key + ' se encuentra conectado.\n').encode('ascii'))


def send_data(sender, receiver, message):
    """Sends messages from a sender to a receiver."""
    if receiver in CONNECTION_DICT:
        sock = CONNECTION_DICT.get(receiver)
        sock.send(message.encode('ascii'))
    else:
        sock = CONNECTION_DICT.get(sender)
        sock.send(('\r' + receiver + ' no conectado.\n').encode('ascii'))


def listen_client(client_id, client_socket):
    """Listen the client and redirects its messages to other clients."""
    size = 1024
    client_socket.send(
        ('Bienvenido al Chat ' + client_id + '\n').encode('ascii'))
    send_connected_clients(client_socket)
    while True:
        data = client_socket.recv(size).decode('ascii')
        if data:
            if data.find('>') > -1:
                receiver, message = data.split('>')
                send_data(client_id, receiver, '\r<' +
                          client_id + '> ' + message)
            else:
                broadcast_data(client_id, '\r<' + client_id + '> ' + data)


if __name__ == "__main__":
    HOST = ''
    PORT = 8888
    CONNECTION_LIST = []
    CONNECTION_DICT = {}
    CLIENT_COUNTER = 0
    SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        SERVER_SOCKET.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    THREADS = []
    SERVER_SOCKET.listen(10)
    CONNECTION_LIST.append(SERVER_SOCKET)
    CONNECTION_DICT.update({'Server': SERVER_SOCKET})

    while 1:
        READ_SOCKETS, WRITE_SOCKETS, ERROR_SOCKETS = select.select(
            CONNECTION_LIST, [], [])
        for socket in READ_SOCKETS:
            if socket == SERVER_SOCKET:
                connection, address = SERVER_SOCKET.accept()
                client = 'C' + str(CLIENT_COUNTER + 1)
                CONNECTION_LIST.append(connection)
                CONNECTION_DICT.update({client:connection})
                THREADS.append(threading.Thread(target=listen_client,
                                                args=(client, connection, )).start())
                broadcast_data(client, '\r' + client + ' entro al chat\n')
                CLIENT_COUNTER += 1

    SERVER_SOCKET.close()
