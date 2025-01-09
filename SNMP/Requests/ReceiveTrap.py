import socket
from Protocol.packet_utils import encodeASN1, decodeASN1
from tkinter import messagebox

def ReceiveTrap():
    while 1:
        agentIp = '127.0.0.1'
        bufferSize = 1024
        conn = bytearray(agentIp, "utf-8")
        UDPclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        UDPclient.bind((conn, 8081))
        while 1:
            data = UDPclient.recvfrom(bufferSize)[0]
            decoded = decodeASN1(data)
            val = decoded[2]
            oid = decoded[0]
            if oid[0] == 0:
                print("TRAP: RAM % IS: ", val)
                messagebox.showwarning("TRAP", "RAM % IS bigger than 50!!!")
                break
            elif oid[0] == 1:
                print("TRAP: CPU % IS: ", val)
                messagebox.showwarning("TRAP", "CPU % IS bigger than 50!!!")
                break