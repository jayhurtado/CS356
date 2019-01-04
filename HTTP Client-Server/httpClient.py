# Http client
# Jason Hurtado
# UCID: jh465
# Section: 003

from datetime import datetime, timezone
import sys, re, time
from socket import*

#socketAPI.pdf

# localhost:12000/filename.html
argv = sys.argv
url = argv[1] #web url containing hostname and port where server is running
# and name of the file to be downloaded
splitURL = url.split("/") #https://www.geeksforgeeks.org/python-string-split/
fileName = splitURL[1]
hostName = splitURL[0]
temp = hostName.split(":")
port = int(temp[1])
host = temp[0]

    #conditional GET requests
    #time.sleep(15) #https://stackoverflow.com/questions/510348/how-can-i-make-a-time-delay-in-python
try:
    cachedfile = open("cache.txt", "r")
    contents = cachedfile.read()
    cachedfile.close()
    lastmod = open("lastmod.txt", "r")
    last_mod_time = lastmod.read()
    lastmod.close()

    sendData = "GET /"+fileName+ " HTTP/1.1\r\n"
    #print(sendData)
    sendData += "Host: "+hostName+ "\r\n"
    sendData += "If-Modified-Since: "+last_mod_time+"\r\n"
    sendData += "\r\n"
    print("Conditional GET request: "+sendData)
    clientSocket2 = socket(AF_INET, SOCK_STREAM)
    clientSocket2.connect((host,port))
    clientSocket2.send(sendData.encode())
    serverResponse2 = clientSocket2.recv(4096)
    serverContents2 = serverResponse2.decode()

    #if server indicates that the file hasnt been modified since last downloaded
    #print contents saying so
    if "304 Not Modified" in serverContents2:
        print(serverContents2+"\n")
        clientSocket2.close()
    #else print and cache new contents
    else:
        splitServerContents2 = serverContents2.split("\r\n")
        #print(splitServerContents2[0])
        #print(splitServerContents2[1])
        lengthTwo = len(splitServerContents2)
        fileContents2 = splitServerContents2[lengthTwo-1]
        print(serverContents2+"\n")
        #print(fileContents+"\n")
        if "404 Not Found" in serverContents2:
            exit()
        else:
            temp = serverContents2.split("Last-Modified: ")
            temp2 = temp[1].split("\r\n")
            last_mod_time = temp2[0]

            lastmod = open("lastmod.txt", "w")
            lastmod.write(last_mod_time)
            lastmod.close()
        #cache the file in cache.txt
            cacheFile2 = open("cache.txt", "w")
            cacheFile2.write(fileContents2)
            cacheFile2.close()
            clientSocket2.close()
except FileNotFoundError:

    sendData = "GET /"+fileName+ " HTTP/1.1\r\n"
    sendData += "Host: "+hostName+ "\r\n"
    sendData += "\r\n"

    clientSocket = socket(AF_INET, SOCK_STREAM)
    #print("Connecting to "+host+","+str(port))
    clientSocket.connect((host,port))

    print("Sending data to server: " +sendData)
    clientSocket.send(sendData.encode())

    serverResponse = clientSocket.recv(4096) #https://docs.python.org/3.4/howto/sockets.html
    serverContents = serverResponse.decode()
    #split it into serverContents and fileContents seperately
    if "404 Not Found" in serverContents:
        print(serverContents+"\n") #should be header contents
    else:
        splitServerContents = serverContents.split("\r\n")
        lengthOne = len(splitServerContents) #https://stackoverflow.com/questions/22101086/split-and-count-a-python-string
        #print(len)
        fileContents = splitServerContents[lengthOne-1]
        print(serverContents+"\n")
        #print(fileContents+"\n")

    #cache the file in cache.txt
        cacheFile = open("cache.txt", "w")
        cacheFile.write(fileContents)
        cacheFile.close()
        clientSocket.close()

        temp = serverContents.split("Last-Modified: ")
        temp2 = temp[1].split("\r\n")
        last_mod_time = temp2[0]

        lastmod = open("lastmod.txt", "w")
        lastmod.write(last_mod_time)
        lastmod.close()
