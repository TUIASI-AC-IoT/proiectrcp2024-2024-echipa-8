import socket
from pyasn1.codec.ber import encoder, decoder
from pyasn1.type import univ
from pdu import *
from encoding import *

def send_snmp_message(snmp_message, target_ip, target_port):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(snmp_message, (target_ip, target_port))
    print(f"Mesaj trimis către {target_ip}:{target_port}")

    sock.close()


def main():
    version = 0  # SNMPv1
    community = 'public'

    # Creăm un PDU de test (de exemplu, GetRequestPDU)
    get_request_pdu = GetRequestPDU()
    get_request_pdu.setComponentByName('request-id', 1)
    get_request_pdu.setComponentByName('error-status', 'noError')
    get_request_pdu.setComponentByName('error-index', 0)
    var_bind_list = VarBindList()
    var_bind = VarBind()
    var_bind.setComponentByName('name', univ.ObjectIdentifier('1.3.6.1.2.1.1.1.0'))
    var_bind.setComponentByName('value', univ.Null())
    var_bind_list.setComponentByPosition(0, var_bind)
    get_request_pdu.setComponentByName('variable-bindings', var_bind_list)

    # Codificăm mesajul SNMP
    encoded_message = encode_snmp_message(version, community, get_request_pdu)

    # Adresa IP și portul agentului SNMP
    agent_ip = '127.0.0.1'  # IP-ul agentului (poți modifica)
    agent_port = 161  # Portul standard SNMP (161)

    # Trimitem mesajul SNMP prin UDP
    send_snmp_message(encoded_message, agent_ip, agent_port)


if __name__ == "__main__":
    main()
