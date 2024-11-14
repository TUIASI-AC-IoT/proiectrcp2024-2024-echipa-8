from pyasn1.codec.ber import encoder, decoder
from pyasn1.type import univ, namedtype, namedval
from pdu import *

def encode_snmp_message(version, community, pdu):
    message = Message()
    message.setComponentByName('version', version)
    message.setComponentByName('community', community)
    message.setComponentByName('data', pdu)
    encoded_message = encoder.encode(message)
    return encoded_message

def decode_snmp_message(encoded_message, pdu_class):
    decoded_message, _ = decoder.decode(encoded_message, asn1Spec=Message())
    version = decoded_message.getComponentByName('version')
    community = decoded_message.getComponentByName('community')

    pdu_data = decoded_message.getComponentByName('data')

    pdu_type_mapping = {
        GetRequestPDU: GetRequestPDU(),
        GetNextRequestPDU: GetNextRequestPDU(),
        GetResponsePDU: GetResponsePDU(),
        SetRequestPDU: SetRequestPDU(),
        TrapPDU: TrapPDU()
    }

    decoded_pdu, _ = decoder.decode(pdu_data.asOctets(), asn1Spec=pdu_type_mapping[pdu_class])

    return version, community, decoded_pdu

def create_and_test_pdu(pdu, version, community):
    encoded_message = encode_snmp_message(version, community, pdu)
    print("\nMesaj SNMP codificat:", encoded_message)

    pdu_class = pdu.__class__
    decoded_version, decoded_community, decoded_pdu = decode_snmp_message(encoded_message, pdu_class)

    print("Mesaj SNMP decodificat:")
    print("Version:", decoded_version)
    print("Community:", decoded_community)
    print("PDU:", decoded_pdu.prettyPrint())

def main():
    version = 0  # SNMPv1
    community = 'public'

    # Testăm GetRequestPDU
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
    create_and_test_pdu(get_request_pdu, version, community)

    # Testăm GetNextRequestPDU
    get_next_request_pdu = GetNextRequestPDU()
    get_next_request_pdu.setComponentByName('request-id', 2)
    get_next_request_pdu.setComponentByName('error-status', 'noError')
    get_next_request_pdu.setComponentByName('error-index', 0)
    get_next_request_pdu.setComponentByName('variable-bindings', var_bind_list)
    create_and_test_pdu(get_next_request_pdu, version, community)

    # Testăm GetResponsePDU
    get_response_pdu = GetResponsePDU()
    get_response_pdu.setComponentByName('request-id', 3)
    get_response_pdu.setComponentByName('error-status', 'noSuchName')
    get_response_pdu.setComponentByName('error-index', 1)
    get_response_pdu.setComponentByName('variable-bindings', var_bind_list)
    create_and_test_pdu(get_response_pdu, version, community)

    # Testăm SetRequestPDU
    set_request_pdu = SetRequestPDU()
    set_request_pdu.setComponentByName('request-id', 4)
    set_request_pdu.setComponentByName('error-status', 'noError')
    set_request_pdu.setComponentByName('error-index', 0)
    set_request_pdu.setComponentByName('variable-bindings', var_bind_list)
    create_and_test_pdu(set_request_pdu, version, community)

    # Testăm TrapPDU
    trap_pdu = TrapPDU()
    trap_pdu.setComponentByName('enterprise', univ.ObjectIdentifier('1.3.6.1.4.1.8072.3.2.10'))
    trap_pdu.setComponentByName('agent-addr', univ.OctetString('192.168.1.1'))
    trap_pdu.setComponentByName('generic-trap', 'linkDown')
    trap_pdu.setComponentByName('specific-trap', 0)
    trap_pdu.setComponentByName('time-stamp', 123456)
    trap_pdu.setComponentByName('variable-bindings', var_bind_list)
    create_and_test_pdu(trap_pdu, version, community)


if __name__ == "__main__":
    main()
