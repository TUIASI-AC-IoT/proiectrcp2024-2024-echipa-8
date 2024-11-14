import socket
from pyasn1.codec.ber import decoder
from pyasn1.type import univ
from pdu import *
from encoding import *


def receive_snmp_message(listen_ip, listen_port):
    # creare socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # facem legatura dintre socket cu ip-ul si portul
    sock.bind((listen_ip, listen_port))

    print(f"Agent SNMP ascultă pe {listen_ip}:{listen_port}")

    data, addr = sock.recvfrom(1024)
    print(f"Mesaj primit de la {addr}")

    version, community, decoded_pdu = decode_snmp_message(data, GetRequestPDU)

    print("Mesaj SNMP decodificat:")
    print(f"Version: {version}")
    print(f"Community: {community}")
    print(f"PDU: {decoded_pdu.prettyPrint()}")

    sock.close()


def main():
    listen_ip = '127.0.0.1'
    listen_port = 161
    receive_snmp_message(listen_ip, listen_port)


if __name__ == "__main__":
    main()