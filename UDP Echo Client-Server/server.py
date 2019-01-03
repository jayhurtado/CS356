# Jason Hurtado
# UCID: jh645 Section: 003

import sys
from socket import *

serverIP = "127.0.0.1"
serverPort = 12000
dataLen = 100

s = socket(AF_INET, SOCK_DGRAM)
s.bind((serverIP,serverPort))

print('The server is ready to receive on port: ' +str(serverPort))

while True:

	data,address = s.recvfrom(dataLen)
	print("Receive data from client " +address[0]+", "+str(address[1])+": "+data.decode())

	print("Sending data to client "+address[0]+", "+str(address[1])+": "+data.decode())
	s.sendto(data,address)
