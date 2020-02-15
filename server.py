#!/usr/bin/env python

ServerSettings = {
    "RequiresAuth" : False
}
PORT = 42069
HOST = '' # all availabe interfaces

import socket, sys, random, string
from _thread import start_new_thread
CloseServer = False
GlobalBroadcastPackets = []
Clients = []

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
print("[SCAM-Server main thread] Server is ready for connections.")

# New clients start a new thread of this function.
def client_thread(conn, addr):
    global CloseServer, GlobalBroadcastPackets
    clientid = "[" + addr[0] + ":" + str(addr[1]) + "] "
    print(clientid+"Client Connected.")
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
        try:
            print(clientid+"Recieved Packet "+data.decode("utf-8"))
        except Exception as e:
            print(clientid+"An Exception occurred: "+str(e))
            print(clientid+"This probably happened because the client did not close the connection properly.")
        PacketQueue, ClientSettings, CloseConnection, CloseServer, GlobalBroadcastPackets = parsePacket(data.decode("utf-8"), ClientSettings, ServerSettings, CloseServer, GlobalBroadcastPackets)
        for Strings in PacketQueue:
            conn.sendall(bytes(Strings, "utf-8"))
            print(clientid + "Sent package with Content: "+Strings)
    conn.close()
    print(clientid+"Client Disconnected, Connection closed.")

def broadcast_thread():
    global GlobalBroadcastPackets, Clients
    while not CloseServer:
        for packetData in GlobalBroadcastPackets:
            print("[Broadcast Thread] Broadcasting packet "+ packetData + " to all clients.")
            GlobalBroadcastPackets.remove(packetData)
            for connection in Clients:
                try:
                    connection.sendall(bytes(packetData, "utf-8"))
                except:
                    Clients.remove(connection)



while not CloseServer:
    # blocking call, waits to accept a connection
    conn, addr = s.accept()
    start_new_thread(client_thread, (conn,addr,)) # Start a new thread for every client.
    Clients.append(conn)
    start_new_thread(broadcast_thread, ()) # Starts sending global broadcasts to all clients.


s.close()
print("[SCAM-Server main thread] Closing server...")