#!/usr/bin/env python

import socket, sys, random, string
from _thread import start_new_thread

ServerSettings = {
    "RequiresAuth" : False
}

HOST = '' # all availabe interfaces
PORT = 42069

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except Exception as e:
    print("Could not create socket: " + str(e))
    sys.exit(0)

print("[SCAM-Server main thread] Socket Created")

# bind socket
try:
    s.bind((HOST, PORT))
    print("[SCAM-Server main thread] Socket Bound to port " + str(PORT))
except Exception as e:
    print("[SCAM-Server main thread] Bind Failed: "+str(e))
    sys.exit()

s.listen(10)
print("[SCAM-Server main thread] Server is ready for conneections.")

# Threading

def client_thread(conn, addr):
    print("[" + addr[0] + ":" + str(addr[1]) + "] Client Connected.")
    from scamlib.parse import parsePacket
    ClientSettings = {
        "Stage" : "PREAUTH",
        "User" : "",
        "Token" : ''.join(random.choices(string.ascii_letters + string.digits, k=24))
    }
    CloseConnection = False

    while not CloseConnection:
        try:
            data = conn.recv(1024)
        except ConnectionResetError:
            break
        if not data:
            break
        print("[" + addr[0] + ":" + str(addr[1]) + "] Recieved Packet "+data.decode("utf-8"))
        PacketQueue, ClientSettings, CloseConnection = parsePacket(data.decode("utf-8"), ClientSettings, ServerSettings)
        for Strings in PacketQueue:
            conn.sendall(bytes(Strings, "utf-8"))
    print("[" + addr[0] + ":" + str(addr[1]) + "] Client Disconnected.")
    conn.close()

while True:
    # blocking call, waits to accept a connection
    conn, addr = s.accept()
    start_new_thread(client_thread, (conn,addr,)) # Start a new thread for every client.

s.close()