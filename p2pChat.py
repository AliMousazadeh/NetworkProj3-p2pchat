import os
import socket
import sys
from threading import Thread
import time
import random

targetDevice = []
BUFFER_SIZE = 4096


def receiveBroadcastMessage():
    while True:
        data, address = receiveBroadcastSocket.recvfrom(BUFFER_SIZE)
        dataStr = data.decode()

        if (dataStr == "hello"):
            if (address not in targetDevice):
                targetDevice.append(address)


def SendBroadcastMessage():
    while True:
        send_message = "hello"
        sendBroadcastSocket.sendto(
            send_message.encode(), ('<broadcast>', 37020))
        time.sleep(1)


def letsChatReceive():
    global tcpSendThread
    global tcpReceiveThread
    while True:
        data, address = sendBroadcastSocket.recvfrom(BUFFER_SIZE)
        dataStr = data.decode().split("-")
        if (dataStr[0] == "let's chat"):
            print("let's chat received")

            tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpSocket.connect((address[0], int(dataStr[1])))

            tcpSendThread = Thread(target=tcpSend, args=(tcpSocket,))
            tcpReceiveThread = Thread(target=tcpReceive, args=(tcpSocket,))

            tcpReceiveThread.start()
            tcpSendThread.start()


def tcpSend(tcpSocket):
    while True:
        dataStr = input()
        data = dataStr.encode()
        tcpSocket.send(data)


def tcpReceive(tcpSocket):
    while True:
        data = tcpSocket.recv(BUFFER_SIZE)
        dataStr = data.decode()
        print(dataStr)


global receiveBroadcastSocket
receiveBroadcastSocket = socket.socket(
    socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
receiveBroadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiveBroadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
receiveBroadcastSocket.bind(("", 37020))

global sendBroadcastSocket
sendBroadcastSocket = socket.socket(
    socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sendBroadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sendBroadcastSocket.bind(("", 0))


global receiveBroadcastThread
global sendBroadcastThread
global letsChatReceiveThread
global tcpSendThread
global tcpReceiveThread

receiveBroadcastThread = Thread(target=receiveBroadcastMessage)
sendBroadcastThread = Thread(target=SendBroadcastMessage)
letsChatReceiveThread = Thread(target=letsChatReceive)


receiveBroadcastThread.start()
sendBroadcastThread.start()
letsChatReceiveThread.start()

while(len(targetDevice) < 2):
    time.sleep(0.1)

s = socket.socket()
s.settimeout(1)
port = random.randint(5000, 6000)
s.bind(('', port))
s.listen()
message = "let's chat-" + str(port)
sendBroadcastSocket.sendto(
    message.encode(), targetDevice[1])
c, addr = s.accept()
print("Connection Established")

tcpSendThread = Thread(target=tcpSend, args=(c,))
tcpReceiveThread = Thread(target=tcpReceive, args=(c,))

tcpSendThread.start()
tcpReceiveThread.start()

tcpReceiveThread.join()
tcpSendThread.join()
