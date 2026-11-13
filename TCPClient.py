
from socket import *

serverName = '192.168.96.128'
serverPort = 5201

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))

sentence = input('Input lowercase sentence: ')
clientSocket.sendall(sentence.encode())

modifiedSentence = clientSocket.recv(1024).decode()

print('From Server:', modifiedSentence)

clientSocket.close()
