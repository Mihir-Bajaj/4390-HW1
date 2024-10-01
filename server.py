import socket

#define the host/port
httpHost = "127.0.0.1"
httpPort = 8080
def readFile(fileName):
     try:
          with open(fileName, 'r') as file:
               content = file.read()
               return content
     except IOError:
          raise IOError
def startServer():
     #define socket using AF_INET to correspond with ipv4
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

     #bind socket to host/port
     s.bind((httpHost, httpPort))

     #set socket to listen once
     s.listen(1)
     print("listening at port:", httpPort )

     #accept incoming connection
     cn, addr = s.accept()
     print("connected to: ", cn, ":", addr)

     try:
          #recieve HTTP request 
          req = cn.recv(1024)
          req = req.decode('utf-8')
          print("request received: ", req) 

          #split request into array
          arr = req.split()
          #set filename to first value in array using [1:] to substring and remove '/'
          fName = arr[1][1:]
          print ("filename", fName) 
          #if no file name given set fName to index
          if fName == '':
               fName = 'index.html'
          content = readFile(fName)

          #HTTP 200 response
          response = 'HTTP/1.1 200 OK\r\n'
          response +=  "Content-Length: " + str(len(content)) +"\r\n\r\n"
          response += content
          
     except IOError:
          #HTTP 400/404 response
          response = 'HTTP/1.1 404 Not Found\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>'
     #send response
     response = response.encode('utf-8')
     cn.sendall(response)

     #close connection
     cn.close()
     