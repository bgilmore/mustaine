import datetime
import time
from array import array
from collections import namedtuple
from struct import pack, unpack
from types import *

ENCODERS = {}
DECODERS = {}

def handle(data_type):
    def register(f):
        # register function `f` to encode type `data_type`
        if f.__name__.startswith("encode_"):
            ENCODERS[data_type] = f
        else:
            DECODERS[data_type] = f
        return f
    return register

def encode_object(value):
    if type(value) in ENCODERS:
        encoder = ENCODERS[type(value)]
        return encoder(value)
    else:
        raise TypeError("Mustaine cannot serialize {0}".format(type(value)))


class HessianCall(object):
    def __init__(self, method, args=None):
        self._buffer = array('c', 'H\x02\x00')
        self._buffer.extend(pack('cB', 'C', len(method)) + method)
        self._buffer.extend(pack('B', 0x90 + len(args)))

        for arg in args:
            self._buffer.extend(encode_object(arg))

    def __len__(self):
        return len(self._buffer)

    def __str__(self):
        return self._buffer.tostring()

## TYPE ENCODERS ##

@handle(NoneType)
def encode_null(value):
    # null       ::= 'N'
    return 'N'

@handle(BooleanType)
def encode_bool(value):
    # boolean    ::= 'T'|'F'
    if value:
        return 'T'
    else:
        return 'F'

@handle(IntType)
def encode_int(value):
    # int        ::= 'I' b3 b2 b1 b0
    return pack('<cl', 'I', value)

@handle(LongType)
def encode_long(value):
    # long       ::= 'L' b7 b6 b5 b4 b3 b2 b1 b0
    return pack('<cq', 'L', value)

@handle(FloatType)
def encode_double(value):
    # double     ::= 'D' b7 b6 b5 b4 b3 b2 b1 b0
    return pack('<cd', 'D', value)

@handle(StringType)
def encode_string(value):
    # string     ::= x52 b1 b0 <utf8-data> string  # non-final chunk
    #            ::= 'S' b1 b0 <utf8-data>         # string of length
    #                                              #  0-65535
    string = ''

    # append non-final chunks
    while len(value) > 65535:
        string += pack('<BH', 0x52, 65535)
        string += value[:65535]
        value   = value[65535:]

    # append final chunk
    string += pack('<cH', 'S', len(value))
    string += value

    return string

@handle(UnicodeType)
def encode_utf8(value):
    return encode_string(value.encode('utf-8'))

@handle(ListType)
def encode_list(value):
    # list       ::= x57 value* 'Z'               # variable-length untyped list
    return '\x57' + ''.join(map(encode_object, value)) + 'Z'

@handle(TupleType)
def encode_tuple(value):
    # list       ::= x58 int value*               # fixed-length untyped list
    return '\x58' + ''.join(map(encode_object, (len(value),) + value))

@handle(DictType)
def encode_dict(value):
    # map        ::= 'H' (value value)* 'Z'       # untyped key, value
    def encode_item(key, val):
        return ''.join((encode_object(key), encode_object(val)))
    
    return 'H' + ''.join(map(encode_item, value.keys(), value.values())) + 'Z'

@handle(datetime.datetime)
def encode_date(value):
    # date       ::= x4a b7 b6 b5 b4 b3 b2 b1 b0
    return pack('<BQ', 0x4a, int(time.mktime(value.timetuple())) * 1000)


# @handle(BooleanType)
# def decode_bool(value):
#     if value == 'T':
#         return True
#     else:
#         return False
# 
# @handle(datetime.datetime)
# def decode_date(value)
#     timestamp = int(unpack('xQ', value)[0] / 1000)
#     return datetime.datetime.fromtimestamp(timestamp)
