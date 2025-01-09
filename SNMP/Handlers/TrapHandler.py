import time
import socket
import psutil
from Protocol.packet_utils import encodeASN1, decodeASN1


def checkTrap():
    agentIp = '127.0.0.1'
    conn = bytearray(agentIp, "utf-8")

    UDPagent = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    while 1:
        ramPercent = psutil.virtual_memory()[2]

        if ramPercent > 50:
            encoded_message = encodeASN1(oid="0.0", text="RAM", val=ramPercent)
            UDPagent.sendto(encoded_message, (conn, 8081))

        cpuPercent = psutil.cpu_percent(4)

        if cpuPercent > 50:
            encoded_message = encodeASN1(oid="1.0", text="CPU", val=cpuPercent)
            UDPagent.sendto(encoded_message, (conn, 8081))

        time.sleep(1)