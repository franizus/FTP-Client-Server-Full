import socket


HOST = 'localhost'   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

#create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#now connect to the web server on port 80
# - the normal http port
print 'connecting to ' + HOST + ':' + str(PORT)
s.connect((HOST, PORT))

for i in range(5):
    # Send data
    message = 'Mensaje.'
    print 'sending ' + message
    s.send(message)
    data = s.recv(16)
    print 'received ' + data

print 'closing socket'
s.close()
