import blynklib
import blynktimer
import socket
import sys
from sense_hat import SenseHat


BLYNK_AUTH = 'c3bUKILDyi0R_dXa4hr3el77KoLYW49b'
UDP_IP_RELAY = "192.168.137.2"
UDP_IP_AN_SENSOR_1 = "192.168.137.3"
UDP_IP_AN_SENSOR_2 = "192.168.137.4"
UDP_PORT1 = 8888
UDP_PORT2 = 9999

# initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

# create timers dispatcher instance
timer = blynktimer.Timer()

# initialize socket
sock0 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# register handler for virtual pin V0 write event
@blynk.handle_event('write V0')
def write_virtual_pin_handler(pin, value):
	try:
		sock0.settimeout(1)
		message = str(value[0])
		print('Module 1 ->  '+ message)
		sock0.sendto(message.encode('utf-8'), (UDP_IP_RELAY, UDP_PORT1))
		data0, address = sock0.recvfrom(4096)
		print("Reply: ", data0.decode('utf-8'), "from: ", address)
	except:
		print("An exception occurred writing to module 1")

# Use blynk timer to send analog value on time bases
@timer.register(pin=2, interval=5, run_once=False)
def write_to_virtual_pin(pin=2):
	try:
		sock2.settimeout(1)
		message = "temperature"
		print('Module 2 -> '+ message)
		sock2.sendto(message.encode('utf-8'), (UDP_IP_AN_SENSOR_1, UDP_PORT1))
		data2, address = sock2.recvfrom(16)
		print("Reply: ", data2.decode('utf-8'), "from: ", address)
		blynk.virtual_write(2, data2.decode('utf-8'))

	except:
		print("An exception occurred reading from module 2 - temperature")
		blynk.virtual_write(pin, "---")

# Use blynk timer to send analog value on time bases
@timer.register(pin=3, interval=5, run_once=False)
def write_to_virtual_pin(pin=3):
	try:
		sock3.settimeout(1)
		message = "humidity"
		print('Module 2 -> '+ message)
		sock3.sendto(message.encode('utf-8'), (UDP_IP_AN_SENSOR_1, UDP_PORT2))
		data3, address = sock3.recvfrom(16)
		print("Reply: ", data3.decode('utf-8'), "from: ", address)
		blynk.virtual_write(pin, data3.decode('utf-8'))
	except:
		print("An exception occurred reading from module 2 - humidity")
		blynk.virtual_write(pin, "---")

# Use blynk timer to send analog value on time bases
@timer.register(pin=4, interval=5, run_once=False)
def write_to_virtual_pin(pin=4):
	try:
		sock4.settimeout(1)
		message = "light"
		print('Module 3 -> '+ message)
		sock4.sendto(message.encode('utf-8'), (UDP_IP_AN_SENSOR_2, UDP_PORT1))
		data4, address = sock4.recvfrom(16)
		print("Reply: ", data4.decode('utf-8'), "from: ", address)
		blynk.virtual_write(pin, data4.decode('utf-8'))
	except:
		print("An exception occurred reading from module 3 - light")
		blynk.virtual_write(pin, "---")




# infinite loop that waits for event
while True:
    blynk.run()
    timer.run()
