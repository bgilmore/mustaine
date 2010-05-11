# transparent types used for hessian serialization
# objects of this type can appear on the wire but have no native python type

class HessianCall(object):
    def __init__(self, method, args=None, headers=None, overload=False):
        self.method   = method
        self.args     = args or ()
        self.headers  = headers or {}
        self.overload = overload
        if not isinstance(self.headers, dict):
            raise TypeError("HessianCall headers must be passed as a dict")

    def __repr__(self):
        return "<mustaine.protocol.HessianCall({0}, ...)>".format(self.method)


class HessianReply(object):
    def __init__(self, result):
        self._result = result

    def __repr__(self):
        return "<mustaine.protocol.HessianReply>"


class HessianFault(Exception):
    def __init__(self, code, message):
        self.code    = code
        self.message = message

    def __repr__(self):
        return "<mustaine.protocol.HessianFault [{0}: {1}]>".format(self.code, self.message)

    def __str__(self):
        return self.__repr__()

class HessianBinary(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "<mustaine.protocol.HessianBinary({0})>".format(self.value)


class HessianRemote(object):
    def __init__(self, type_name, url):
        self.type_name = type_name
        self.url       = url

    def __repr__(self):
        return "<mustaine.protocol.HessianRemote({0}, {1})>".format(self.type_name, self.url)

