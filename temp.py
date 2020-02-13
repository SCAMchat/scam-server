#!/usr/bin/env python

import socket


TCP_IP = '192.168.178.13'
TCP_PORT = 42069
BUFFER_SIZE = 4096  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address:'+str(addr))
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print("received data:"+str(data))
    conn.send(data)  # echo
conn.close()