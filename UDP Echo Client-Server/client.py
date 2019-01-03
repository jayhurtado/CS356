# Jason Hurtado 
# UCID: jh465 Section: 003

import sys, time
from socket import*

argv = sys.argv 
serverhost = argv[1]
serverport = argv[2]
datalength = argv[3]

serverport = int(serverport)
datalength = int(datalength)
data = 'J'* datalength

s = socket(AF_INET, SOCK_DGRAM)
s.settimeout(1)
x=0
while x < 3:
	try:
		print("Sending data to "+serverhost+", "+str(serverport)+": " +data+ " ( " +str(datalength)+ " characters)")
		s.sendto(data.encode(),(serverhost,serverport))


		dataEcho,address = s.recvfrom(datalength)

		print("Receive data from " +address[0]+", "+str(address[1])+": "+dataEcho.decode())
		break

	except Exception as e:
		print("the message timed out")
		x+=1





s.close()
