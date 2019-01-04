# Jason Hurtado
# UCID jh465, Section 003

import random
import struct
import sys
from socket import *

serverIP = "127.0.0.1"
serverPort = 12000

s = socket(AF_INET, SOCK_DGRAM)
s.bind((serverIP,serverPort))

print("The server is ready to receive on port: "+str(serverPort))
	
while True:
	data, address = s.recvfrom(serverPort)
	seqnum = struct.unpack('!ii', data)[1] #https://docs.python.org/3/library.struct.html
	rand = random.randrange(10) #https://docs.python.org/3/library/random.html#random.random
	if rand < 4:
		print("Message with sequence number "+str(seqnum)+ " dropped")
	else:
		print("Responding to ping request with sequence number "+str(seqnum))
		data = struct.pack('!ii', 2, seqnum)
		s.sendto(data,address)
		
	


