#!/usr/bin/python3.7 

# This is a very simple sockets server
import socket
from sense_hat import SenseHat


# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Set host and port
host = "192.168.1.14"
port = 9999

# bind the socket object to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

# Create SenseHAT object (used to access temp sensor)
sense = SenseHat()

print("Listening for TCP Connection on port %s" %  str(port))

while True:
   # accept/establish connection
   clientsocket,addr = serversocket.accept()
   print("Got a connection from %s" % str(addr))
   #get data sent from connection (decapsulated from TCP segment(s)) and show on SenseHAT
   data = clientsocket.recv(1024)
   sense.show_message(data.decode('ascii'))
   clientsocket.close()
