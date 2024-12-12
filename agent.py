from encoding import *
from socket import *

AGENT_IP = "127.0.0.1"
AGENT_PORT = 161

OID_DATABASE = {
    (1, 3, 6, 1, 2, 1, 1, 1, 0): "Simulated SNMP Agent"
}

def handle_request(request_pdu):
    pdu_type, request_id, error_status, error_index, var_bind_list = request_pdu

    response_var_bind_list = []
    for oid, value in var_bind_list:
        if tuple(oid) in OID_DATABASE:
            response_var_bind_list.append((oid, OID_DATABASE[tuple(oid)]))
        else:
            response_var_bind_list.append((oid, "OID not found"))

    response_pdu = encode_pdu(0xA2, request_id, 0, 0, response_var_bind_list)  # 0xA2 = GetResponse
    return response_pdu

def main():
    with socket(AF_INET, SOCK_DGRAM) as sock:
        sock.bind((AGENT_IP, AGENT_PORT))
        print("Agent SNMP asculta pe portul", AGENT_PORT)

        while True:
            request_data, addr = sock.recvfrom(4096)
            print("Cerere primita:", request_data)

            version, community, request_pdu = decode_message(request_data)
            print("Versiune:", version)
            print("Comunitate:", community)
            print("Request PDU:", request_pdu)

            response_pdu = handle_request(request_pdu)
            response_message = encode_message(version, community, response_pdu)

            sock.sendto(response_message, addr)
            print("Raspuns trimis:", response_message)

if __name__ == "__main__":
    main()

