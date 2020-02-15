
def checkAuth(uname,passwd):
    return True

def parsePacket(packetString, ClientSettings, ServerSettings, CloseServer, GlobalBroadcastPackets):
    packetQueue = []
    CloseConnection = False

    # Before a user tries to login.

    if ClientSettings["Stage"] == "PREAUTH":
        if packetString == "HELLO":
            if ServerSettings["RequiresAuth"]:
                packetQueue.append("HELLO AUTH")
            else:
                packetQueue.append("HELLO NOAUTH")
            ClientSettings["Stage"] = "PRELOGIN"
        else:
            packetQueue.append("100")

    # User can now try login.

    elif ClientSettings["Stage"] == "PRELOGIN":
        if packetString[0:4] == "USER": # get username
            ClientSettings["User"] = packetString[6:]
            packetQueue.append("OKAY")
        if ServerSettings["RequiresAuth"]: # get password, if required
            if packetString[0:4] == "PASS" and ClientSettings["User"] != "": # if user has username set and is trying to set pass?
                if checkAuth(ClientSettings["User"],packetString[6:]): # check if username and passs are valid
                    packetQueue.append("OKAY")
                    packetQueue.append(ClientSettings["Token"])
                    ClientSettings["Stage"] = "ServerConnection"
                else: # login failed.
                    packetQueue.append("301")
                    CloseConnection = True
            else: # didnt folllow the protocol
                packetQueue.append("200")
        else: # liogin uiser without password as server does not need auth.
            packetQueue.append(ClientSettings["Token"])
            ClientSettings["Stage"] = "ServerConnection"
    
    elif "ServerConnection" in ClientSettings["Stage"] :
        if packetString[0:3] == "MSG" and packetString[-3:] == "END":
            message = packetString[4:]
            packetQueue.append("OKAY")
            GlobalBroadcastPackets.append("UPDATE\n"+message)
        
    else:
        packetQueue.append("100")
    return packetQueue, ClientSettings, CloseConnection, CloseServer, GlobalBroadcastPackets