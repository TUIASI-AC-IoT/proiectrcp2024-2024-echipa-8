from encoding import *
from socket import *

AGENT_IP = "127.0.0.1"
AGENT_PORT = 161

def main():
    request_id = 1
    var_bind_list = [([1, 3, 6, 1, 2, 1, 1, 1, 0], "")]
    pdu = encode_pdu(0xA0, request_id, 0, 0, var_bind_list)
    message = encode_message(1, "public", pdu)

    with socket(AF_INET, SOCK_DGRAM) as sock:
        sock.sendto(message, (AGENT_IP, AGENT_PORT))
        print("Mesaj trimis catre agent:", message)

        response_data, _ = sock.recvfrom(4096)
        print("Raspuns primit de la agent:", response_data)

        version, community, response_pdu = decode_message(response_data)
        pdu_type, request_id, error_status, error_index, var_bind_list = response_pdu

        print("Versiune:", version)
        print("Comunitate:", community)
        print("PDU Type:", pdu_type)
        print("Request ID:", request_id)
        print("Error Status:", error_status)
        print("Error Index:", error_index)
        print("VarBind List:", var_bind_list)

if __name__ == "__main__":
    main()


