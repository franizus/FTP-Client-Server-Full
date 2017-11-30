import socket
import sys
 
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8889 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
(conn, addr) = s.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])

file = open("server_code.txt", "r")
for line in file:
    conn.send(line)
else:
    conn.send("file finished")

file.close()
s.close()
