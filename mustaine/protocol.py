import datetime
import time
from array import array
from collections import namedtuple
from struct import pack, unpack
from types import *

from mustaine.encoder import encode_object
# from mustaine.parser import parse_bytecode

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

