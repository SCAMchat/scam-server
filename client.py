#!/usr/bin/env python

import socket


TCP_IP = '192.168.178.13'
TCP_PORT = 42069
BUFFER_SIZE = 4096
MESSAGE = bytes(input("Message? >"), "utf-8")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print("received data:"+str(data))