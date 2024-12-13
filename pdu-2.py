
class ErrorStatus:
    values = {
        'noError': 0,
        'tooBig': 1,
        'noSuchName': 2,
        'badValue': 3,
        'readOnly': 4,
        'genErr': 5
    }

    def __init__(self, value='noError'):
        if value not in self.values:
            raise ValueError("Invalid ErrorStatus")
        self.value = self.values[value]


class RequestID:
    def __init__(self, value):
        if not isinstance(value, int):
            raise TypeError("RequestID must be an integer")
        self.value = value


class ErrorIndex:
    def __init__(self, value):
        if not isinstance(value, int):
            raise TypeError("ErrorIndex must be an integer")
        self.value = value


class VarBind:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class VarBindList:
    def __init__(self):
        self.varbinds = []

    def add(self, varbind):
        if not isinstance(varbind, VarBind):
            raise TypeError("Only VarBind instances can be added")
        self.varbinds.append(varbind)


class GetRequestPDU:
    def __init__(self, request_id, var_bind_list):
        self.request_id = RequestID(request_id)
        self.error_status = ErrorStatus('noError')
        self.error_index = ErrorIndex(0)
        self.variable_bindings = var_bind_list


class GetNextRequestPDU(GetRequestPDU):
    pass


class GetResponsePDU:
    def __init__(self, request_id, error_status, error_index, var_bind_list):
        self.request_id = RequestID(request_id)
        self.error_status = ErrorStatus(error_status)
        self.error_index = ErrorIndex(error_index)
        self.variable_bindings = var_bind_list


class SetRequestPDU(GetRequestPDU):
    pass


class TrapPDU:
    def __init__(self, enterprise, agent_addr, generic_trap, specific_trap, time_stamp, var_bind_list):
        self.enterprise = enterprise
        self.agent_addr = agent_addr
        self.generic_trap = generic_trap
        self.specific_trap = specific_trap
        self.time_stamp = time_stamp
        self.variable_bindings = var_bind_list


class Message:
    def __init__(self, version, community, data):
        self.version = version
        self.community = community
        self.data = data
