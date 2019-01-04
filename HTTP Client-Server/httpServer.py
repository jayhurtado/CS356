# Jason Hurtado
# UCID: jh465 Section: 003
#http server

from datetime import datetime, timezone
import sys, os.path, re, time
from socket import*
serverIP = "127.0.0.1" #localhost
serverPort = 12000
dataLen = 1000000

#socketAPI.pdf
#all time and date from programming hints and https://docs.python.org/3/library/datetime.html

#current time in UTC/GMT timezone and convert to string in HTTP format
t = datetime.now(timezone.utc)
#print(t)
date = datetime.strftime(t, "%a, %d %b %Y %H:%M:%S %Z\r\n")
#print(date)

serverSocket = socket(AF_INET, SOCK_STREAM)
#bind is optional for TCP
serverSocket.bind((serverIP, serverPort))
#listen for incoming connection requests
serverSocket.listen(1)

#print("The server is ready to listen on port "+str(serverPort))

while True:
    connectionSocket, address = serverSocket.accept()

    #assuming file exists
    data = connectionSocket.recv(4096).decode()
    retrievedData = re.split('\s|/', data) #https://w3resource.com/python-exercises/re/python-re-exercise-47.php
    fileName = retrievedData[2]


    try:
            #getting files modification time in seconds
        modTime = os.path.getmtime(fileName)
            #convert above time to UTC/GMT(returns a time tuple)
        modTimeUTC = time.gmtime(modTime)
            #convert to a string in HTTP format
        last_mod_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT", modTimeUTC)


        htmlFile = open(fileName, "r")
        fileContents = htmlFile.read()
        #https://stackoverflow.com/questions/30686701/python-get-size-of-string-in-bytes
        dataLen = len(fileContents.encode('utf-8')) #length in bytes
        #print(data)
        #conditional response message(NotModified)
        #if not modified send this. else send the original response

        if "If-Modified-Since: " in data:
            #print(data)
            #print("got this far")
            temp = data.split("If-Modified-Since: ")
            temp2 = temp[1].split("\r\n")
            modifiedSinceTime = temp2[0]
            #print(modifiedSinceTime)
            #print(last_mod_time)
            if last_mod_time == modifiedSinceTime:
                responseData = "HTTP/1.1 304 Not Modified\r\n"
                responseData += "Date: "+date+"\r\n"
                responseData += "\r\n"
                connectionSocket.send(responseData.encode())
                connectionSocket.close()
            else:
                responseData = "HTTP/1.1 200 OK\r\n"
                responseData += "Date: "+date+"\r\n"
                responseData += "Last-Modified: "+last_mod_time+"\r\n"
                responseData += "Content-Length: "+str(dataLen)+"\r\n"
                responseData += "Content-Type: text/html; charset=UTF-8\r\n"
                responseData += "\r\n"
                responseData += fileContents
                #print(responseData)
                connectionSocket.send(responseData.encode())
                connectionSocket.close()

        else:

            responseData = "HTTP/1.1 200 OK\r\n"
            responseData += "Date: "+date+"\r\n"
            responseData += "Last-Modified: "+last_mod_time+"\r\n"
            responseData += "Content-Length: "+str(dataLen)+"\r\n"
            responseData += "Content-Type: text/html; charset=UTF-8\r\n"
            responseData += "\r\n"
            responseData += fileContents

            connectionSocket.send(responseData.encode())
            connectionSocket.close()
            #close the file maybe
    #https://dbader.org/blog/python-check-if-file-exists
    except FileNotFoundError:
            #HTTP server Response when file not found
        responseData = "HTTP/1.1 404 Not Found\r\n"
        responseData += "Date: "+date+"\r\n"
        responseData += "\r\n"
        connectionSocket.send(responseData.encode())
        connectionSocket.close()
        #sending tthe response header and the contents(body) of the requested file
