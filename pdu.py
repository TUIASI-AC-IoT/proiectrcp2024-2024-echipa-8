from pyasn1.type import univ, namedtype, constraint, namedval


class ErrorStatus(univ.Integer):
    namedValues = namedval.NamedValues(
        ('noError', 0),
        ('tooBig', 1),
        ('noSuchName', 2),
        ('badValue', 3),
        ('readOnly', 4),
        ('genErr', 5)
    )


class RequestID(univ.Integer):
    pass


class ErrorIndex(univ.Integer):
    pass


class VarBind(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('name', univ.ObjectIdentifier()),
        namedtype.NamedType('value', univ.Any())
    )


class VarBindList(univ.SequenceOf):
    componentType = VarBind()

# Definim structurile PDU pentru GetRequest, GetNextRequest, GetResponse, SetRequest si Trap
class GetRequestPDU(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('request-id', RequestID()),
        namedtype.NamedType('error-status', ErrorStatus().subtype(value='noError')),
        namedtype.NamedType('error-index', ErrorIndex()),
        namedtype.NamedType('variable-bindings', VarBindList())
    )

class GetNextRequestPDU(GetRequestPDU):
    pass

class GetResponsePDU(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('request-id', RequestID()),
        namedtype.NamedType('error-status', ErrorStatus()),
        namedtype.NamedType('error-index', ErrorIndex()),
        namedtype.NamedType('variable-bindings', VarBindList())
    )

class SetRequestPDU(GetRequestPDU):
    pass


class TrapPDU(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('enterprise', univ.ObjectIdentifier()),
        namedtype.NamedType('agent-addr', univ.OctetString()),
        namedtype.NamedType('generic-trap', univ.Integer(namedValues=namedval.NamedValues(
            ('coldStart', 0), ('warmStart', 1), ('linkDown', 2), ('linkUp', 3),
            ('authenticationFailure', 4), ('egpNeighborLoss', 5), ('enterpriseSpecific', 6)
        ))),
        namedtype.NamedType('specific-trap', univ.Integer()),
        namedtype.NamedType('time-stamp', univ.Integer()),
        namedtype.NamedType('variable-bindings', VarBindList())
    )


class Message(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('version', univ.Integer(namedValues=namedval.NamedValues(('version-1', 0)))),
        namedtype.NamedType('community', univ.OctetString()),
        namedtype.NamedType('data', univ.Any())
    )


