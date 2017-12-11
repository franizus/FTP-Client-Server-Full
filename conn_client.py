import socket
import sys
import select


def prompt():
    sys.stdout.write('>>> ')
    sys.stdout.flush()


if __name__ == "__main__":
    if(len(sys.argv) < 3) :
        print('Usage : python conn_client.py hostname port')
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try :
        s.connect((host, port))
    except :
        print('No se puede conectar')
        sys.exit()

    while 1:
        socket_list = [sys.stdin, s]
        read_sockets, ws, es = select.select(socket_list, [], [])
        for sock in read_sockets:
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    print('\nDesconectado del servidor de chat.')
                    sys.exit()
                else:
                    sys.stdout.write(data.decode('ascii'))
                    prompt()
            else:
                msg = sys.stdin.readline()
                s.send(msg.encode('ascii'))
                prompt()

    s.close()