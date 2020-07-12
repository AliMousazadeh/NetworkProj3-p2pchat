from socket import *

SEND_PORT = 12345
RECV_PORT = SEND_PORT + 1

sendSocket = socket(AF_INET, SOCK_DGRAM)
sendSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
recvSocket = socket(AF_INET, SOCK_DGRAM)
recvSocket.bind(('', RECV_PORT))

print("Broadcasting Hello...")
sendSocket.sendto("Hello".encode(), ('255.255.255.255', SEND_PORT))
message, address = recvSocket.recvfrom(1024)
print("{}: {}".format(address, message.decode()))

while True:
    message, address = recvSocket.recvfrom(1024)
    print("{}: {}".format(address, message.decode()))
