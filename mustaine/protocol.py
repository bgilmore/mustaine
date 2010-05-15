# transparent types used for hessian serialization
# objects of this type can appear on the wire but have no native python type

class Call(object):
    def __init__(self, method=None, args=None, headers=None, overload=None):
        self._method   = method or ''
        self._args     = args or list()
        self._headers  = headers or dict()
        self._overload = overload or False

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        if isinstance(value, str):
            self._method = value
        else:
            raise TypeError("Call.method must be a string")

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        if hasattr(value, '__iter__'):
            self._args = value
        else:
            raise TypeError("Call.args must be an iterable value")

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        if not isinstance(value, dict):
            raise TypeError("Call.headers must be a dict of strings to objects")

        for key in value.keys():
            if not isinstance(key, basestring):
                raise TypeError("Call.headers must be a dict of strings to objects")

        self._headers = value

    @property
    def overload(self):
        return self._overload

    @overload.setter
    def overload(self, value):
        if isinstance(value, bool):
            self._overload = value
        else:
            raise TypeError("Call.overload must be True or False")


class Reply(object):
    def __init__(self, value=None, headers=None):
        self.value    = value # unmanaged property
        self._headers = headers or dict()

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        if not isinstance(value, dict):
            raise TypeError("Call.headers must be a dict of strings to objects")

        for key in value.keys():
            if not isinstance(key, basestring):
                raise TypeError("Call.headers must be a dict of strings to objects")

        self._headers = value


class Fault(Exception):
    def __init__(self, code=None, message=None, detail=None):
        self.code    = code
        self.message = message
        self.detail  = detail


class Binary(object):
    def __init__(self, value):
        self.value = value


class Remote(object):
    def __init__(self, type_name=None, url=None):
        self.type_name = type_name
        self.url       = url

