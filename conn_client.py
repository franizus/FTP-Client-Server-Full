""" Concurrent Chat Client module """
import socket
import sys
import select


def prompt():
    """Prints a prompt to the console to send messages."""
    sys.stdout.write('>>> ')
    sys.stdout.flush()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage : python conn_client.py hostname port')
        sys.exit()

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        CLIENT_SOCKET.connect((HOST, PORT))
    except socket.error as msg:
        print('Connection failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    SOCKET_LIST = [sys.stdin, CLIENT_SOCKET]
    while True:
        READ_SOCKETS, WRITE_SOCKETS, ERROR_SOCKETS = select.select(SOCKET_LIST, [], [])
        for socket in READ_SOCKETS:
            if socket == CLIENT_SOCKET:
                data = socket.recv(4096)
                if not data:
                    print('\nDesconectado del servidor de chat.')
                    sys.exit()
                else:
                    sys.stdout.write(data.decode('ascii'))
                    prompt()
            else:
                msg = sys.stdin.readline()
                CLIENT_SOCKET.send(msg.encode('ascii'))
                prompt()

    CLIENT_SOCKET.close()
