from network import LoRa
import socket
import utime
import binascii
import pycom
import ustruct
import machine
import time
import json

# LED Color constants and meaning
ON = 0xFFFFFF
OFF = 0x000000
RED = 0xFF0000 # Not Connected to LoRa Gateway
GREEN = 0x00FF00 # Connected to LoRa Gateway
BLUE = 0x0000FF # Valid Sensor Read and transmission
ORANGE = 0xFFA500 # Invalid Sensor Read

# LED start-up routine
pycom.rgbled(ON)
time.sleep_ms(200)
pycom.rgbled(OFF)
time.sleep_ms(50)
pycom.rgbled(GREEN)
time.sleep_ms(200)
pycom.rgbled(OFF)
time.sleep_ms(50)
pycom.rgbled(ON)
time.sleep_ms(200)
pycom.rgbled(OFF)
time.sleep_ms(100)

# set LED to red
pycom.rgbled(0x7f0000)

# lora config
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
# access info
app_eui = binascii.unhexlify('70B3D57ED001FD3F')
app_key = binascii.unhexlify('7C344DD6E2BBAA4DBF29FB13DE79D30F')

# attempt join - continues attempts background
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait for a connection
print('Waiting for LoRaWAN network connection...')
while not lora.has_joined():
	utime.sleep(1)
	# if no connection in a few seconds, then reboot
	if utime.time() > 15:
		print("possible timeout")
		machine.reset()
	pass

# we're online, set LED to green and notify via print
pycom.rgbled(0x007f00)
print('Network joined!')

# setup the socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(False)
s.bind(1)

while True:
    # Sensor Read
	result = th.read()
	if result.is_valid():
		pycom.rgbled(BLUE)
		print("\nTemperature: %d C" % result.temperature)
		print("Humidity: %d %%" % result.humidity)
		# Send data (only if result is valid)
		results = [result.temperature, result.humidity]
		print("\nSending sensor reads.")
		s.send(bytes([result.temperature, result.humidity]))
	else:
		pycom.rgbled(ORANGE)
		print("\nInvalid sensor read result.")
		results = [24, 41]
		print("\nSending test bytes.")
		s.send(bytes([results[0], results[1]]))
	time.sleep_ms(500)
	pycom.rgbled(OFF) # turn OFF LED
	time.sleep_ms(500)
	pycom.rgbled(0x013B0C) # set it to green while connected
	time.sleep(20) # wait for new transmission
	pycom.rgbled(OFF) # turn OFF LED
	time.sleep_ms(500)
