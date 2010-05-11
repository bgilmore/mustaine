import datetime
import time
from struct import pack, unpack

from types import *
from mustaine.protocol import *

# Implementation of Hessian 1.0.2 serialization
#   see: http://hessian.caucho.com/doc/hessian-1.0-spec.xtp

ENCODERS = {}
def encoder_for(data_type):
    def register(f):
        # register function `f` to encode type `data_type`
        ENCODERS[data_type] = f
        return f
    return register

def returns(data_type):
    def wrap(f):
        # wrap function `f` to return a tuple of (type,data)
        def wrapped(*args):
            return data_type, f(*args)
        return wrapped
    return wrap

def encode_object(obj):
    if type(obj) in ENCODERS:
        encoder = ENCODERS[type(obj)]
        return encoder(obj)[1]
    else:
        raise TypeError("mustaine.encoder cannot serialize {0}".format(type(obj)))


@encoder_for(NoneType)
@returns('null')
def encode_null(value):
    return 'N'

@encoder_for(BooleanType)
@returns('bool')
def encode_boolean(value):
    if value:
        return 'T'
    else:
        return 'F'

@encoder_for(IntType)
@returns('int')
def encode_int(value):
    return pack('>cl', 'I', value)

@encoder_for(LongType)
@returns('long')
def encode_long(value):
    return pack('>cq', 'L', value)

@encoder_for(FloatType)
@returns('double')
def encode_double(value):
    return pack('>cd', 'D', value)

@encoder_for(datetime.datetime)
@returns('date')
def encode_date(value):
    return pack('>cq', 'd', int(time.mktime(value.timetuple())) * 1000)

@encoder_for(StringType)
@returns('string')
def encode_string(value):
    encoded = ''

    try:
        value = value.encode('ascii')
    except UnicodeDecodeError:
        raise TypeError("mustaine.encoder cowardly refuses to guess the encoding for "
                        "string objects containing bytes out of range 0x00-0x79; use "
                        "HessianBinary or unicode objects instead")

    while len(value) > 65535:
        encoded += pack('>cH', 's', 65535)
        encoded += value[:65535]
        value    = value[65535:]

    encoded += pack('>cH', 'S', len(value.decode('utf-8')))
    encoded += value
    return encoded

@encoder_for(UnicodeType)
@returns('string')
def encode_unicode(value):
    encoded = ''

    while len(value) > 65535:
        encoded += pack('>cH', 's', 65535)
        encoded += value[:65535].encode('utf-8')
        value    = value[65535:]

    encoded += pack('>cH', 'S', len(value))
    encoded += value.encode('utf-8')
    return encoded

@encoder_for(ListType)
@returns('list')
def encode_list(obj):
    encoded = ''.join(map(encode_object, obj))
    return pack('>2cl', 'V', 'l', -1) + encoded + 'z'

@encoder_for(TupleType)
@returns('list')
def encode_tuple(obj):
    encoded = ''.join(map(encode_object, obj))
    return pack('>2cl', 'V', 'l', len(obj)) + encoded + 'z'

@encoder_for(DictType)
@returns('map')
def encode_map(obj):
    def encode_pair(pair):
        return ''.join((encode_object(pair[0]), encode_object(pair[1])))

    encoded = ''.join(map(encode_pair, obj.items()))
    return pack('>c', 'M') + encoded + 'z'

@encoder_for(HessianRemote)
@returns('map')
def encode_remote(obj):
    encoded = encode_string(obj.url)
    return pack('>2cH', 'r', 't', len(obj.type_name)) + obj.type_name + encoded

@encoder_for(HessianBinary)
@returns('binary')
def encode_binary(obj):
    encoded = ''
    value   = obj.value

    while len(value) > 65535:
        encoded += pack('>cH', 'b', 65535)
        encoded += value[:65535]
        value    = value[65535:]

    encoded += pack('>cH', 'B', len(value))
    encoded += value

    return encoded

@encoder_for(HessianCall)
@returns('call')
def encode_call(call):
    method    = call.method
    headers   = ''
    arguments = ''

    for header,value in call.headers.items():
        if not isinstance(header, StringType):
            raise TypeError("HessianCall header keys must be strings")

        headers += pack('>cH', 'H', len(header)) + header
        headers += encode_object(value)

    for arg in call.args:
        if type(arg) in ENCODERS:
            data_type, arg = ENCODERS[type(arg)](arg)
            if call.overload:
                method    += '_' + data_type
            arguments += arg

    encoded  = pack('>cBB', 'c', 1, 0)
    encoded += headers
    encoded += pack('>cH', 'm', len(method)) + method
    encoded += arguments
    encoded += 'z'
    
    return encoded

