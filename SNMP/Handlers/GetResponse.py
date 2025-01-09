from Utils.mib_utils import MIB
from Protocol.packet_utils import encodeASN1


def GetResponse(OID, address, UDPAgent):
    while True:
        if not OID: break
        print(OID)

        if OID[0][1] == 1:
            print(MIB.Temperature)
            temperatura = MIB.get_temperatura(MIB.Temperature)

            if temperatura is not None:
                print(temperatura)
                encoded_message = encodeASN1(oid="1.1", text="Null", val=temperatura)
                UDPAgent.sendto(encoded_message, address)
            else:
                encoded_message = encodeASN1(oid="1.1", text="Null", val=0.0)
                UDPAgent.sendto(encoded_message, address)
            break

        elif OID[0][1] == 2:
            encoded_message = encodeASN1(oid="1.2", text=MIB.Name, val=0)
            UDPAgent.sendto(encoded_message, address)
            break

        elif OID[0][1] == 3:
            ram_percent = MIB.getRamPercent(MIB.getData)
            encoded_message = encodeASN1(oid="1.3", text="Null", val=ram_percent)
            UDPAgent.sendto(encoded_message, address)
            break

        elif OID[0][1] == 4:
            ram_gb = MIB.getRamGB(MIB.getData)
            encoded_message = encodeASN1(oid="1.4", text="Null", val=ram_gb)
            UDPAgent.sendto(encoded_message, address)
            break

        elif OID[0][1] == 5:
            cpu_percent = MIB.getCPUPercent(MIB.getData)
            encoded_message = encodeASN1(oid="1.5", text="Null", val=cpu_percent)
            UDPAgent.sendto(encoded_message, address)
            break

        else:
            UDPAgent.sendto(bytes("Invalid", "utf-8"), address)
            break