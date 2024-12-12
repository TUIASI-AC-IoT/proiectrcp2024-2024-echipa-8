def encode_integer(value):
    if not isinstance(value, int):
        raise TypeError("Value must be an integer")
    if value < 0:
        raise ValueError("ASN.1 INTEGER must be non-negative in this implementation")

    result = bytearray()
    while value > 0:
        result.insert(0, value & 0xFF)
        value >>= 8

    if not result:
        result.append(0)

    length = len(result)
    return bytes([0x02, length]) + bytes(result)


def decode_integer(data):
    if data[0] != 0x02:
        raise ValueError("Invalid ASN.1 INTEGER type")
    length = data[1]
    if len(data) < 2 + length:
        raise ValueError("Data too short for specified length")

    value = 0
    for i in range(2, 2 + length):
        value = (value << 8) | data[i]

    return value


def encode_string(value):
    if not isinstance(value, str):
        raise TypeError("Value must be a string")
    encoded_value = value.encode('utf-8')
    length = len(encoded_value)
    return bytes([0x04, length]) + encoded_value


def decode_string(data):
    if data[0] != 0x04:
        raise ValueError("Invalid ASN.1 STRING type")
    length = data[1]
    if len(data) < 2 + length:
        raise ValueError("Data too short for specified length")
    return data[2:2 + length].decode('utf-8')


def encode_oid(oid):
    if not isinstance(oid, list) or len(oid) < 2 or not all(isinstance(i, int) for i in oid):
        raise TypeError("OID must be a list of integers with at least two elements")
    result = bytearray()
    result.append(40 * oid[0] + oid[1])
    for sub_id in oid[2:]:
        if sub_id < 0:
            raise ValueError("OID sub-identifiers must be non-negative")
        sub_result = []
        while sub_id > 0:
            sub_result.insert(0, (sub_id & 0x7F) | 0x80)
            sub_id >>= 7
        if not sub_result:
            sub_result.append(0)
        sub_result[-1] &= 0x7F
        result.extend(sub_result)
    length = len(result)
    return bytes([0x06, length]) + bytes(result)


def decode_oid(data):
    if data[0] != 0x06:
        raise ValueError("Invalid ASN.1 OID type")
    length = data[1]
    if len(data) < 2 + length:
        raise ValueError("Data too short for specified length")
    oid = []
    first_byte = data[2]
    oid.append(first_byte // 40)
    oid.append(first_byte % 40)
    value = 0
    for i in range(3, 2 + length):
        if data[i] & 0x80:
            value = (value << 7) | (data[i] & 0x7F)
        else:
            value = (value << 7) | data[i]
            oid.append(value)
            value = 0
    return oid


def encode_pdu(pdu_type, request_id, error_status, error_index, var_bind_list):
    encoded_request_id = encode_integer(request_id)
    encoded_error_status = encode_integer(error_status)
    encoded_error_index = encode_integer(error_index)

    encoded_var_bind_list = b''.join([
        encode_oid(varbind[0]) + encode_string(varbind[1])
        for varbind in var_bind_list
    ])

    total_length = (
        len(encoded_request_id) +
        len(encoded_error_status) +
        len(encoded_error_index) +
        len(encoded_var_bind_list)
    )

    return bytes([pdu_type, total_length]) + \
           encoded_request_id + \
           encoded_error_status + \
           encoded_error_index + \
           encoded_var_bind_list


def decode_pdu(data):
    if len(data) < 2:
        raise ValueError("Data too short for PDU decoding")

    pdu_type = data[0]
    length = data[1]
    if len(data) != 2 + length:
        raise ValueError("PDU length mismatch")

    offset = 2

    request_id = decode_integer(data[offset:])
    offset += 2 + data[offset + 1]

    error_status = decode_integer(data[offset:])
    offset += 2 + data[offset + 1]

    error_index = decode_integer(data[offset:])
    offset += 2 + data[offset + 1]

    var_bind_list = []
    while offset < len(data):
        oid = decode_oid(data[offset:])
        oid_length = 2 + data[offset + 1]
        offset += oid_length

        value = decode_string(data[offset:])
        value_length = 2 + data[offset + 1]
        offset += value_length

        var_bind_list.append((oid, value))

    return pdu_type, request_id, error_status, error_index, var_bind_list


def encode_message(version, community, pdu):
    encoded_version = encode_integer(version)
    encoded_community = encode_string(community)
    total_length = len(encoded_version) + len(encoded_community) + len(pdu)
    return bytes([0x30, total_length]) + encoded_version + encoded_community + pdu

def decode_message(data):
    if data[0] != 0x30:
        raise ValueError("Invalid data type for message")
    length = data[1]
    version = decode_integer(data[2:])
    community_start = 2 + len(data[2:2 + data[3]]) + 2
    community = decode_string(data[community_start:])
    pdu_start = community_start + len(data[community_start:community_start + data[community_start + 1]]) + 2
    pdu = data[pdu_start:2 + length]
    return version, community, decode_pdu(pdu)
