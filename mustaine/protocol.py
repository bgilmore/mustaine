from struct import pack, unpack
from types import *

class HessianFault(Exception):
    """ Raised when a Hessian error occurs """
    def __init__(self, code, msg, **detail):
        self.code = code
        self.msg  = msg
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return "<HessianFault: '{1}: {2}'".format(self.code, self.msg)

class HessianDecoder:
    def __init__(self, f):
        self._f = f
        self._peek = -1
        # self.read = f.read
        self._refs = []

    def read(self, len):
        if self._peek >= 0:
          value = self._peek
          self._peek = -1
          return value
        else:
          return self._f.read(len)

    def parse_reply(self):
        # parse header 'c' x01 x00 'v' ... 'z'
        read = self.read
        firstByte = read(1)
        if firstByte != 'r':
            print "Invalid first byte response: %s" % (firstByte, )
            self.error()
        major = read(1)
        minor = read(1)

        value = self.parse_object()

        if read(1) == 'z':
            return value
        self.error() # actually a fault

    def parse_object(self):
        # parse an arbitrary object based on the type in the data
        return self.parse_object_code(self.read(1))

    def parse_object_code(self, code):
        # parse an object when the code is known
        read = self.read

        if code == 'N':
            return None

        elif code == 'T':
            return True

        elif code == 'F':
            return False

        elif code == 'I':
            return unpack('>l', read(4))[0]

        elif code == 'L':
            return unpack('>q', read(8))[0]

        elif code == 'D':
            return unpack('>d', read(8))[0]

        elif code == 'd':
            ms = unpack('>q', read(8))[0]

            return Date(int(ms / 1000.0))

        elif code == 'S' or code == 'X':
            return self.parse_string()

        elif code == 'B':
            return Binary(self.parse_string())

        elif code == 'V':
            self.parse_type() # skip type
            self.parse_length()           # skip length
            list = []
            self._refs.append(list)
            
            ch = read(1)
            while ch != 'z':
                list.append(self.parse_object_code(ch))
                ch = read(1)
            
            return list

        elif code == 'M':
            self.parse_type() # skip type
            map = {}
            self._refs.append(map)
            
            ch = read(1)
            while ch != 'z':
                key = self.parse_object_code(ch)
                value = self.parse_object()
                map[key] = value
                ch = read(1)
                
            return map

        elif code == 'R':
            return self._refs[unpack('>l', read(4))[0]]

        elif code == 'r':
            self.parse_type()       # skip type
            url = self.parse_type() # reads the url
            return Hessian(url)
        
        elif code =='f':
            # fault
            self.parse_type() # skip type
            map = {}
            self._refs.append(map)
            
            ch = read(1)
            while ch != 'z':
                key = self.parse_object_code(ch)
                value = self.parse_object()
                map[key] = value
                ch = read(1)
                
            raise HessianFault(map['code'], map['message'])
            
        elif code == None:
                raise RuntimeError, "No Code!"
        else:
            raise RuntimeError, "UnknownObjectCode %s" % code

    def parse_string(self):
        f = self._f
        len = unpack('>H', f.read(2))[0]
        
        bytes = []
        while len > 0:
            byte = self.read(1)
            if ord(byte) in range(0x00, 0x7F):
                bytes.append(byte)
            elif ord(byte) in range(0xC2, 0xDF):
                bytes.append(byte + self.read(1))
            elif ord(byte) in range(0xE0, 0xEF):
                bytes.append(byte + self.read(2))
            elif ord(byte) in range(0xF0, 0xF4):
                bytes.append(byte + self.read(3))
            len -= 1
        
        return ''.join(bytes).decode('utf-8')

    def parse_type(self):
        f = self._f
        code = self.read(1)
        if code != 't':
          self._peek = code
          return ""
        len = unpack('>H', f.read(2))[0]
        return f.read(len)

    def parse_length(self):
        f = self._f
        code = self.read(1);
        if code != 'l':
          self._peek = code
          return -1;
        len = unpack('>l', f.read(4))
        return len

    def error(self):
        raise RuntimeError, "FOO"


class HessianEncoder:
    dispatch = {}

    def __call__(self, method, params):
        self.refs = {}
        self.ref = 0
        self.__out = []
        self.write = write = self.__out.append

        write("c\x01\x00m");
        write(pack(">H", len(method)));
        write(method);
        
        for v in params:
            self.write_object(v)
            
        write("z");
        
        result = ''.join(self.__out)
        del self.__out, self.write, self.refs
        return result

    def write_object(self, value):
        try:
            f = self.dispatch[type(value)]
        except KeyError:
            raise TypeError, "cannot write %s objects" % type(value)
        else:
            f(self, value)

    def write_null(self, value):
        if value != None:
            raise TypeError, "Trying to write None with a value of type %s" % type(value)
        else:
            self.write('N')
    
    dispatch[NoneType] = write_null
    
    def write_int(self, value):
        self.write('I')
        self.write(pack(">l", value))
    
    dispatch[IntType] = write_int

    def write_long(self, value):
        self.write('L')
        self.write(pack(">q", value))
    
    dispatch[LongType] = write_long

    def write_double(self, value):
        self.write('D')
        self.write(pack(">d", value))
        
    dispatch[FloatType] = write_double

    def write_string(self, value):
        self.write('S')
        self.write(pack('>H', len(value)))
        self.write(value.encode('utf-8'))
    
    dispatch[StringType]  = write_string
    dispatch[UnicodeType] = write_string

    def write_bool(self, value):
        if value == True or value > 0:
            self.write('T')
        else:
            self.write('F')
    
    dispatch[BooleanType] = write_bool
    
    def write_reference(self, value):
        # check for and write circular references
        # returns 1 if the object should be written, i.e. not a reference
        i = id(value)
        if self.refs.has_key(i):
            self.write('R')
            self.write(pack(">L", self.refs[i]))
            return 0
        else:
            self.refs[i] = self.ref
            self.ref = self.ref + 1
            return 1

    def write_list(self, value):
        if self.write_reference(value):
            self.write("Vt\x00\x00I");
            self.write(pack('>l', len(value)))
            for v in value:
                self.write_object(v)
            self.write('z')
    
    dispatch[TupleType] = write_list
    dispatch[ListType] = write_list

    def write_map(self, value):
        if self.write_reference(value):
            self.write("Mt\x00\x00")
            for k, v in value.items():
                self.write_string(k)
                self.write_object(v)
            self.write("z")
            
    dispatch[DictType] = write_map

    def write_instance(self, value):
        # check for special wrappers
        if hasattr(value, "_hessian_write"):
            value._hessian_write(self)
        else:
            fields = value.__dict__
            if self.write_reference(fields):
                self.write("Mt\x00\x00")
                for k, v in fields.items():
                    self.write_string(k)
                    self.write_object(v)
                self.write("z")
    
    dispatch[InstanceType] = write_instance

