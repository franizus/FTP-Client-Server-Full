import socket
import sys
from datetime import datetime


def send(connection, address, line, log, i):
    connection.send(line)
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.write("server_code.txt" + "\t" + addr[0] + ':' + str(addr[1]) + "\t" + time + "\t" + str(i) + "\n")
 
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
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
log = open("log.txt", "w")
i = 0

for line in file:
    send(conn, addr, line, log, i)
    i += 1
else:
    conn.send("file finished")

file.close()
s.close()
