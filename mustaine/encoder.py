import datetime
import time
from struct import pack, unpack
from types import *

# Implementation of Hessian 1.0.2 serialization
#   see: http://hessian.caucho.com/doc/hessian-1.0-spec.xtp

ENCODERS = {}
def encoder_for(data_type):
    def register(f)
        # register function `f` to encode type `data_type`
        ENCODERS[data_type] = f
        return f
    return register

def encode_object(obj):
    if type(obj) in ENCODERS:
        encoder = ENCODERS[type(obj)]
        return encoder(obj)
    else:
        raise TypeError("mustaine.encoder cannot serialize {0}".format(type(obj)))

@encoder_for(NoneType)
def encode_null(value):
    return 'N'

@encoder_for(BooleanType)
def encode_boolean(value):
    if value:
        return 'T'
    else:
        return 'F'

@encoder_for(IntType)
def encode_int(value):
    return pack('>cl', 'I', value)

@encoder_for(LongType)
def encode_long(value):
    return pack('>cq', 'L', value)

@encoder_for(FloatType)
def encode_double(value):
    return pack('>cd', 'D', value)

@encoder_for(datetime.datetime)
def encode_date(value):
    return pack('>cq', 'd', int(time.mktime(value.timetuple())) * 1000)

@encoder_for(StringType)
def encode_string(value):
    encoded = ''

    while len(value) > 65535:
        encoded += pack('>cH', 's', 65535)
        encoded += value[:65535]
        value    = value[65535:]

    encoded += pack('>cH', 'S', len(value))
    encoded += value

    return encoded

@encoder_for(UnicodeType)
def encode_unicode(value):
    return encode_string(value.encode('utf-8'))


@encode_for(ListType)
def encode_list(obj):
    encoded = ''.join(map(encode_object, obj))
    return pack('>2cl', 'V', 'l', -1) + encoded + 'z'

@encode_for(TupleType)
def encode_tuple(obj):
    encoded = ''.join(map(encode_object, obj))
    return pack('>2cl', 'V', 'l', len(obj)) + encoded + 'z'

@encode_for(DictType)
def encode_map(obj):
    def encode_pair(pair):
        return ''.join(encode_object(pair[0]), encode_object(pair[1]))

    encoded = ''.join(map(encode_pair, obj.items()))
    return pack('>c', 'M') + encoded + 'z'

