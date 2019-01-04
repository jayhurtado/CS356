#Jason Hurtado
#UCID: jh465 , Section 003

#import random
import struct
import sys, time
from socket import*

argv = sys.argv
serverhost = argv[1]
serverport = argv[2]

serverport = int(serverport)


s = socket(AF_INET, SOCK_DGRAM)
s.settimeout(1)

x=1
while x < 11:
	print("Pinging "+serverhost+", "+str(serverport)+":")
	data = struct.pack('!ii', 1, x) #https://docs.python.org/3/library/struct.html
	beforerequest = time.time() #https://docs.python.org/3/library/time.html
	s.sendto(data,(serverhost,serverport))
	try:
		
		dataEcho,address = s.recvfrom(serverport)
		RTT = time.time() - beforerequest
		#dataEcho.decode()
		print("Ping message number "+str(x)+" RTT: "+str(RTT)+ " seconds")
		x+=1

	except Exception as e:
		print("Ping message "+str(x)+" timed out")
		x+=1


s.close()
