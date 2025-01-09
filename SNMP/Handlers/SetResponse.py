from Utils.mib_utils import MIB
from Protocol.packet_utils import encodeASN1


def SetResponse(OID,address, UDPAgent, text):

    while 1:
        if not OID: break
        if (OID[0][1] == 1):
            MIB.Name=text
            encoded_message = encodeASN1(oid="2.1", text=MIB.Name, val=0)
            UDPAgent.sendto(encoded_message, address)
            break

        elif(OID[0][1] == 2):
            MIB.Temperature = text
            encoded_message = encodeASN1(oid="2.2", text=MIB.Temperature, val=0)
            UDPAgent.sendto(encoded_message, address)
            break
        else:
            UDPAgent.sendto(bytes("Invalid", "utf-8"), address)
            break