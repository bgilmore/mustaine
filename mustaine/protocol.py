from array import array
from collections import namedtuple
from struct import pack, unpack
from types import *

ENCODERS = {}
DECODERS = {}

class HessianCall(object):
    def __init__(self, method, args=None):
        self._buffer = array('c', 'H\x02\x00')
        self._buffer.extend(pack('cB', 'C', len(method)) + method)
        self._buffer.extend(pack('B', 0x90 + len(args)))

        for arg in args:
            if type(arg) in ENCODERS:
                encoder = ENCODERS[type(arg)]
                self._buffer.extend(encoder(arg))
            else:
                raise TypeError("Mustaine cannot serialize {0}".format(type(arg)))

    def __len__(self):
        return len(self._buffer)

    def __str__(self):
        return self._buffer.tostring()




def handle(data_type):
    def register(f):
        # register function `f` to encode type `data_type`
        if f.__name__.startswith("encode_"):
            ENCODERS[data_type] = f
        else:
            DECODERS[data_type] = f
        return f
    return register


@handle(BooleanType)
def encode_bool(value):
    if value:
        return 'T'
    else:
        return 'F'

@handle(BooleanType)
def decode_bool(value):
    if value == 'T':
        return True
    else:
        return False


