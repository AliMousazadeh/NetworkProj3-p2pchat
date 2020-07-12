from socket import *
from threading import Thread


def senderFunction(socket, ip, port):
    while True:
        message = input()
        socket.sendto(message.encode(), (ip, port))


def recieverFunction(socket):
    while True:
        message, address = socket.recvfrom(1024)
        print("{}: {}".format(address, message.decode()))


RECV_PORT = 12345
SEND_PORT = RECV_PORT + 1

recvSocket = socket(AF_INET, SOCK_DGRAM)
recvSocket.bind(('', RECV_PORT))
sendSocket = socket(AF_INET, SOCK_DGRAM)

print("Waiting for Hello...")
message, address = recvSocket.recvfrom(1024)
clientIP = address[0]
print("{}: {}".format(address, message.decode()))
sendSocket.sendto("Let's Chat".encode(), (clientIP, SEND_PORT))

senderThread = Thread(target=senderFunction, args=(
    sendSocket, clientIP, SEND_PORT))
#receiverThread = Thread(target=recieverFunction, args=(recvSocket))

senderThread.start()
# receiverThread.start()
