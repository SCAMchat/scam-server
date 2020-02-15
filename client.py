#!/usr/bin/env python

import socket


TCP_IP = '192.168.178.13'
TCP_PORT = 42069
BUFFER_SIZE = 4096

mesg = "HELLO CLIENT"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while mesg!="exit":
    mesg = input("Message? >")
    s.send(bytes(mesg, "utf-8"))
    data = s.recv(BUFFER_SIZE)
    print("received data:"+str(data))
s.close()
