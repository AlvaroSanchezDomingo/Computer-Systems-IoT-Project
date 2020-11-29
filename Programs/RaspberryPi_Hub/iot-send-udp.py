import socket
import re

UDP_IP = "192.168.1.19"
UDP_PORT =8888 
MESSAGE = "test"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message: ", MESSAGE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
