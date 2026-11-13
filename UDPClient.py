from socket import *
serverName = '192.168.96.128'
serverPort = 5201
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input("Input lowercase sentence: ")

clientSocket.sendto(message.encode(),(serverName, serverPort))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

print("From Server:", modifiedMessage.decode())

print("Server Address:", serverAddress)

clientSocket.close()

