import blynklib
import socket
import sys
from sense_hat import SenseHat


BLYNK_AUTH = 'c3bUKILDyi0R_dXa4hr3el77KoLYW49b'
UDP_IP_RELAY = "192.168.137.1"
UDP_IP_AN_SENSOR_1 = "192.168.137.56"
UDP_PORT = 8888


# initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)
# initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# register handler for virtual pin V0 write event
@blynk.handle_event('write V0')
def write_virtual_pin_handler(pin, value):
	try:
		sock.settimeout(1)
		message = str(value[0])
		print('Relay: '+ message)
		sock.sendto(message.encode('utf-8'), (UDP_IP_RELAY, UDP_PORT))
		data, address = sock.recvfrom(4096)
		print("Reply: ", data.decode('utf-8'), "from: ", address)
	except:
		print("An exception occurred")

# register handler for virtual pin V2(Temperature) reading
@blynk.handle_event('read V2')
def read_virtual_pin_handler(pin):
	try:
		sock.settimeout(1)
		message = "request"
		print('Analog Sensor 1 -> '+ message)
		sock.sendto(message.encode('utf-8'), (UDP_IP_AN_SENSOR_1, UDP_PORT))
		data, address = sock.recvfrom(4096)
		print("Reply: ", data.decode('utf-8'), "from: ", address)
		blynk.virtual_write(pin, data.decode('utf-8'))
	except:
		print("An exception occurred reading analog input 1")
		blynk.virtual_write(pin, "0")

# infinite loop that waits for event
while True:
    blynk.run()
