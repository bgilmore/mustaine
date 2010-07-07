from mustaine import protocol
from mustaine.client import HessianProxy

# Caucho's Hessian 2.0 reference service
# interface: http://caucho.com/resin-javadoc/com/caucho/hessian/test/TestHessian2.html

test = HessianProxy("http://hessian.caucho.com/test/test")

### BINARY ENCODING TESTS DISABLED
# def test_encode_binary_0():
# 	assert test.argBinary_0(protocol.Binary("")) is True
#
# def test_encode_binary_1():
# 	assert test.argBinary_1(protocol.Binary("x")) is True
#
# def test_encode_binary_1023():
# 	assert test.argBinary_1023(protocol.Binary("x" * 1023)) is True
#
# def test_encode_binary_1024():
# 	assert test.argBinary_1024(protocol.Binary("x" * 1024)) is True
#
# def test_encode_binary_15():
# 	assert test.argBinary_15(protocol.Binary("x" * 15)) is True
#
# def test_encode_binary_16():
# 	assert test.argBinary_16(protocol.Binary("x" * 16)) is True
#
# def test_encode_binary_65536():
# 	assert test.argBinary_65536(protocol.Binary("x" * 65536)) is True

### DATE ENCODING TESTS DISABLED, UTC MADNESS
# def test_encode_date_0():
# 	assert test.argDate_0(datetime.datetime(1970, 1, 1)) is True
#
# def test_encode_date_1():
# 	assert test.argDate_1(datetime.datetime(1998, 5, 8, 7, 51)) is True
#
# def test_encode_date_2():
# 	assert test.argDate_1(datetime.datetime(1998, 5, 8, 7, 51)) is True

def test_encode_double_0_0():
	assert test.argDouble_0_0(0.0) is True

def test_encode_double_0_001():
    assert test.argDouble_0_001(0.001) is True

def test_encode_double_1_0():
    assert test.argDouble_1_0(1.0) is True

def test_encode_double_127_0():
    assert test.argDouble_127_0(127.0) is True

def test_encode_double_128_0():
    assert test.argDouble_128_0(128.0) is True

def test_encode_double_2_0():
    assert test.argDouble_2_0(2.0) is True

def test_encode_double_3_14159():
    assert test.argDouble_3_14159(3.14159) is True

def test_encode_double_32767_0():
    assert test.argDouble_32767_0(32767.0) is True

def test_encode_double_65_536():
    assert test.argDouble_65_536(65.536) is True

def test_encode_double_m0_001():
    assert test.argDouble_m0_001(-0.001) is True

def test_encode_double_m128_0():
    assert test.argDouble_m128_0(-128.0) is True

def test_encode_double_m129_0():
    assert test.argDouble_m129_0(-129.0) is True

def test_encode_double_m32768_0():
    assert test.argDouble_m32768_0(-32768.0) is True

def test_encode_false():
    assert test.argFalse(False) is True

def test_encode_int_0():
    assert test.argInt_0(0) is True

def test_encode_int_0x30():
    assert test.argInt_0x30(0x30) is True

def test_encode_int_0x3ffff():
    assert test.argInt_0x3ffff(0x3ffff) is True

def test_encode_int_0x40000():
    assert test.argInt_0x40000(0x40000) is True

def test_encode_int_0x7ff():
    assert test.argInt_0x7ff(0x7ff) is True

def test_encode_int_0x7fffffff():
    assert test.argInt_0x7fffffff(0x7fffffff) is True

def test_encode_int_0x800():
    assert test.argInt_0x800(0x800) is True

def test_encode_int_1():
    assert test.argInt_1(1) is True

def test_encode_int_47():
    assert test.argInt_47(47) is True

def test_encode_int_m0x40000():
    assert test.argInt_m0x40000(-0x40000) is True

def test_encode_int_m0x40001():
    assert test.argInt_m0x40001(-0x40001) is True

def test_encode_int_m0x800():
    assert test.argInt_m0x800(-0x800) is True

def test_encode_int_m0x80000000():
    assert test.argInt_m0x80000000(-0x80000000) is True

def test_encode_int_m0x801():
    assert test.argInt_m0x801(-0x801) is True

def test_encode_int_m16():
    assert test.argInt_m16(-16) is True

def test_encode_int_m17():
    assert test.argInt_m17(-17) is True

def test_encode_long_0():
    assert test.argLong_0(0L) is True

def test_encode_long_0x10():
    assert test.argLong_0x10(0x10L) is True

def test_encode_long_0x3ffff():
    assert test.argLong_0x3ffff(0x3ffffL) is True

def test_encode_long_0x40000():
    assert test.argLong_0x40000(0x40000L) is True

def test_encode_long_0x7ff():
    assert test.argLong_0x7ff(0x7ffL) is True

def test_encode_long_0x7fffffff():
    assert test.argLong_0x7fffffff(0x7fffffffL) is True

def test_encode_long_0x800():
    assert test.argLong_0x800(0x800L) is True

def test_encode_long_0x80000000():
    assert test.argLong_0x80000000(0x80000000L) is True

def test_encode_long_1():
    assert test.argLong_1(1L) is True

def test_encode_long_15():
    assert test.argLong_15(15L) is True

def test_encode_long_m0x40000():
    assert test.argLong_m0x40000(-0x40000L) is True

def test_encode_long_m0x40001():
    assert test.argLong_m0x40001(-0x40001L) is True

def test_encode_long_m0x800():
    assert test.argLong_m0x800(-0x800L) is True

def test_encode_long_m0x80000000():
    assert test.argLong_m0x80000000(-0x80000000L) is True

def test_encode_long_m0x80000001():
    assert test.argLong_m0x80000001(-0x80000001L) is True

def test_encode_long_m0x801():
    assert test.argLong_m0x801(-0x801L) is True

def test_encode_long_m8():
    assert test.argLong_m8(-8L) is True

def test_encode_long_m9():
    assert test.argLong_m9(-9L) is True

def test_encode_null():
    assert test.argNull(None) is True

def test_encode_object_0():
    payload = protocol.Object('com.caucho.hessian.test.A0')
    assert test.argObject_0(payload) is True

def test_encode_object_1():
    payload = protocol.Object('com.caucho.hessian.test.TestObject', _value=0)

    assert test.argObject_1(payload) is True

def test_encode_object_16():
    payload = [
        protocol.Object('com.caucho.hessian.test.A0'),
        protocol.Object('com.caucho.hessian.test.A1'),
        protocol.Object('com.caucho.hessian.test.A2'),
        protocol.Object('com.caucho.hessian.test.A3'),
        protocol.Object('com.caucho.hessian.test.A4'),
        protocol.Object('com.caucho.hessian.test.A5'),
        protocol.Object('com.caucho.hessian.test.A6'),
        protocol.Object('com.caucho.hessian.test.A7'),
        protocol.Object('com.caucho.hessian.test.A8'),
        protocol.Object('com.caucho.hessian.test.A9'),
        protocol.Object('com.caucho.hessian.test.A10'),
        protocol.Object('com.caucho.hessian.test.A11'),
        protocol.Object('com.caucho.hessian.test.A12'),
        protocol.Object('com.caucho.hessian.test.A13'),
        protocol.Object('com.caucho.hessian.test.A14'),
        protocol.Object('com.caucho.hessian.test.A15'),
        protocol.Object('com.caucho.hessian.test.A16')
    ]

    assert test.argObject_16(payload) is True

def test_encode_object_2():
    payload = [
        protocol.Object('com.caucho.hessian.test.TestObject', _value=0),
        protocol.Object('com.caucho.hessian.test.TestObject', _value=1)
    ]

    assert test.argObject_2(payload) is True

def test_encode_object_2a():
    payload = protocol.Object('com.caucho.hessian.test.TestObject', _value=0)

    assert test.argObject_2a([payload, payload]) is True

def test_encode_object_2b():
    payload = [
        protocol.Object('com.caucho.hessian.test.TestObject', _value=0),
        protocol.Object('com.caucho.hessian.test.TestObject', _value=0)
    ]

    assert test.argObject_2b(payload) is True

### argObject_3 causes a stack pop. BOOM, recursion.
# def disabled_test_encode_object_3():
#     payload = protocol.Object('com.caucho.hessian.test.TestCons', _first = 'a', _rest = None)
#     payload._rest = payload
#
#     assert test.argObject_3(payload) is True

def test_encode_string_0():
    assert test.argString_0("") is True

def test_encode_string_1():
    assert test.argString_1("0") is True

def test_encode_string_31():
    payload = "0123456789012345678901234567890"
    assert test.argString_31(payload) is True

def test_encode_string_32():
    payload = "01234567890123456789012345678901"
    assert test.argString_32(payload) is True

### here, we have to generate big convoluted strings. later.
# def test_encode_string_1023():
#     assert test.argString_1023("x" * 1023) is True
#
# def test_encode_string_1024():
#     assert test.argString_1024("x" * 1024) is True
#
# def test_encode_string_65536():
#     assert test.argString_65536("x" * 65536) is True

def test_encode_true():
    assert test.argTrue(True) is True

