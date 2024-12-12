from pyasn1.type import univ, namedtype, constraint, namedval

# Definim variabilele și structurile SNMPv1

# ErrorStatus
class ErrorStatus(univ.Integer):
    namedValues = namedval.NamedValues(
        ('noError', 0),
        ('tooBig', 1),
        ('noSuchName', 2),
        ('badValue', 3),
        ('readOnly', 4),
        ('genErr', 5)
    )

# RequestID și ErrorIndex - sunt INTEGER simple, fără constrângeri suplimentare
class RequestID(univ.Integer):
    pass

class ErrorIndex(univ.Integer):
    pass

# VarBind
class VarBind(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('name', univ.ObjectIdentifier()),
        namedtype.NamedType('value', univ.Any())
    )

# VarBindList - o secvență de VarBind-uri
class VarBindList(univ.SequenceOf):
    componentType = VarBind()

# Definim structurile PDUs pentru GetRequest, GetNextRequest, GetResponse și SetRequest
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

# TrapPDU
class TrapPDU(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('enterprise', univ.ObjectIdentifier()),
        namedtype.NamedType('agent-addr', univ.OctetString()),  # NetworkAddress simplificat
        namedtype.NamedType('generic-trap', univ.Integer(namedValues=namedval.NamedValues(
            ('coldStart', 0), ('warmStart', 1), ('linkDown', 2), ('linkUp', 3),
            ('authenticationFailure', 4), ('egpNeighborLoss', 5), ('enterpriseSpecific', 6)
        ))),
        namedtype.NamedType('specific-trap', univ.Integer()),
        namedtype.NamedType('time-stamp', univ.Integer()),  # simplificare TimeTicks
        namedtype.NamedType('variable-bindings', VarBindList())
    )

# Definim structura de mesaj SNMPv1
class Message(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('version', univ.Integer(namedValues=namedval.NamedValues(('version-1', 0)))),
        namedtype.NamedType('community', univ.OctetString()),
        namedtype.NamedType('data', univ.Any())
    )


