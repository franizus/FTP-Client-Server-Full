import socket


HOST = 'localhost'   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

#create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#now connect to the web server on port 80
# - the normal http port
print 'connecting to ' + HOST + ':' + str(PORT)
s.connect((HOST, PORT))

file = open("server_code_received.txt", "w")
data = s.recv(128)
while data != "file finished":
    file.write(data)
    data = s.recv(128)

file.close()
print 'closing socket'
s.close()
