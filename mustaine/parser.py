import datetime
from collections import namedtuple
from struct import unpack

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from mustaine.protocol import *

# Implementation of Hessian 1.0.2 deserialization
#   see: http://hessian.caucho.com/doc/hessian-1.0-spec.xtp

class ParseError(Exception):
    pass

class Parser(object):
    def from_string(self, string):
        if isinstance(string, UnicodeType):
            stream = StringIO(string.encode('utf-8'))
        else:
            stream = StringIO(string)

        return self.from_stream(stream)

    def from_stream(self, stream):
        self._refs   = []
        self._result = None

        if hasattr(stream, 'read') and hasattr(stream.read, '__call__'):
            self._stream = stream
        else:
            raise TypeError('Stream parser can only handle objects supporting read()')

        while True:
            code = self._read(1)

            if   code == 'c':
                if self._result:
                    raise ParseError('Encountered duplicate type header')

                version = self._read(2)
                if version != '\x01\x00':
                    raise ParseError("Encountered unrecognized call version {0!r}".format(version))

                self._result = Call()
                continue

            elif code == 'r':
                if self._result:
                    raise ParseError('Encountered duplicate type header')

                version = self._read(2)
                if version != '\x01\x00':
                    raise ParseError("Encountered unrecognized reply version {0!r}".format(version))

                self._result = Reply()
                continue

            else:
                if not self._result:
                    raise ParseError("Invalid Hessian message marker: {0!r}".format(code))

                if   code == 'H':
                    key, value = self._read_header()
                    self._result.headers[key] = value
                    continue

                elif code == 'm':
                    if not isinstance(self._result, Call):
                        raise ParseError('Encountered illegal method name within reply')

                    if self._result.method:
                        raise ParseError('Encountered duplicate method name definition')

                    self._result.method = self._read(unpack('>H', self._read(2))[0])
                    continue

                elif code == 'f':
                    if not isinstance(self._result, Reply):
                        raise ParseError('Encountered illegal fault within call')

                    if self._result.value:
                        raise ParseError('Encountered illegal extra object within reply')

                    self._result.value = self._read_fault()
                    continue

                elif code == 'z':
                    break

                else:
                    if isinstance(self._result, Call):
                        self._result.args.append(self._read_object(code))
                    else:
                        if self._result.value:
                            raise ParseError('Encountered illegal extra object within reply')

                        self._result.value = self._read_object(code)

        # have to hit a 'z' to land here, TODO derefs?
        return self._result


    def _read(self, n):
        try:
            r = self._stream.read(n)
        except IOError:
            raise ParseError('Encountered unexpected end of stream')
        except:
            raise
        else:
            if len(r) == 0:
                raise ParseError('Encountered unexpected end of stream')

        return r

    def _read_object(self, code):
        if   code == 'N':
            return None
        elif code == 'T':
            return True
        elif code == 'F':
            return False
        elif code == 'I':
            return int(unpack('>l', self._read(4))[0])
        elif code == 'L':
            return long(unpack('>q', self._read(8))[0])
        elif code == 'D':
            return float(unpack('>d', self._read(8))[0])
        elif code == 'd':
            return self._read_date()
        elif code == 's' or code == 'x':
            fragment = self._read_string() 
            next     = self._read(1)
            if next.lower() == code:
                return fragment + self._read_object(next)
            else:
                raise ParseError("Expected terminal string segment, got {0!r}".format(next))
        elif code == 'S' or code == 'X':
            return self._read_string()

    def _read_date(self):
        timestamp = unpack('>q', self._read(8))[0]
        return datetime.datetime.fromtimestamp(timestamp * 1000)
    
    def _read_string(self):
        len = unpack('>H', self._read(2))[0]
        
        bytes = []
        while len > 0:
            byte = self._read(1)
            if ord(byte) in range(0x00, 0x7F):
                bytes.append(byte)
            elif ord(byte) in range(0xC2, 0xDF):
                bytes.append(byte + self._read(1))
            elif ord(byte) in range(0xE0, 0xEF):
                bytes.append(byte + self._read(2))
            elif ord(byte) in range(0xF0, 0xF4):
                bytes.append(byte + self._read(3))
            len -= 1
        
        return ''.join(bytes).decode('utf-8')
        






# 
# 
# 
# 
# 
# 
# 
# class Message(object):
#     def __new__(
# def parse_message(stream):
#     if isinstance(stream, StringType):
#         stream = StringIO(stream)
#     elif isinstance(stream, UnicodeType):
#         stream = StringIO(stream.encode('utf-8'))
#     else:
#         if not (hasattr(stream, 'read') and hasattr(stream.read, '__call__')):
#             raise TypeError("parse_message can only handle strings and filehandle-type objects")
# 
#     preamble = stream.read(3)
#     if   preamble == 'c\x01\x00':
#         return 
#     elif preamble == 'r\x01\x00':
#         message_type = HessianReply
#     else:
#         raise ParseError("Unrecognized message preamble: {0!r}".format(preamble))
# 
#     code = stream.read(1)
#     if code == 'H':
#         raise NotImplementedError("TODO: add header support")
# 
# 
# 
# 
# 
# 
#     if stream.read(1) == 'H':
#         raise NotImplementedError("TODO: add header support")
#     else:
#         # no headers found, rewind
#         stream.seek(stream.tell() - 1)
#     
#     if message_type == HessianCall:
#         method = read_method(stream)
#         result = HessianCall(method)
#     else:
#         if stream.read(1) == 'f':
#             message_type = HessianFault
# 
