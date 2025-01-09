import threading
from Handlers.GetResponse import GetResponse
from Handlers.SetResponse import SetResponse
from Handlers.TrapHandler import *
from Protocol.packet_utils import decodeASN1

localIP = '127.0.0.1'
localport = 8080
bufferSize = 1024

UDPAgent = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPAgent.bind((localIP, localport))

threading.Thread(target=checkTrap).start()

try:
    while True:
        data = UDPAgent.recvfrom(bufferSize)
        oid = decodeASN1(data[0])
        print("OID este: ", oid[0])

        address = data[1]
        text = oid[1]

        if oid[0][0] == 1:
            GetResponse(oid, address, UDPAgent)
        elif oid[0][0] == 2:
            SetResponse(oid, address, UDPAgent, text)
        else:
            UDPAgent.sendto(bytes("Invalid", "utf-8"), address)
except KeyboardInterrupt:
    print("Agentul a fost oprit manual.")
finally:
    UDPAgent.close()