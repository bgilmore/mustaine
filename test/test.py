
import sys
sys.path.append("..")

import os
import subprocess
import time
import unittest

from mustaine.client import HessianProxy

class TestSimpleClient(unittest.TestCase):
    """
    Integration tests that ensure we're a well-behaved client, and are serializing/deserializing
    simple types well.
    """
        
    def setUp(self):
        self.service = HessianProxy("http://localhost:8080/Test.service")
    
    def test_WriteInt(self):
        self.assertEqual(43, self.service.returnInt(43))

    def test_WriteBool(self):
        self.assertFalse(self.service.returnBool(False))
        self.assertTrue(self.service.returnBool(True))

    def test_WriteLong(self):
        self.assertEqual(43, self.service.returnLong(43))

    def test_WriteDouble(self):
        self.assertEqual(43.5, self.service.returnDouble(43.5))

def buildAndStartJavaServer():
    """
    Builds the Java integration server, and starts embedded Jetty to
    host the Java test services.
    """
        
    args = ["java", "-jar", "server/target/testserver-1.0-jar-with-dependencies.jar"]
    p = subprocess.Popen(args, stderr=subprocess.PIPE)
    
    while True:
      line = p.stderr.readline()
      if "Started SocketConnector" in line:
          break

    return p
    
def stopJavaServer(p):
    """
    Politely asks Jetty to terminate, and waits.
    """
    p.terminate()
    print "Terminated Jetty Server"
    os.wait()

if __name__ == '__main__':
    """
    Builds the Java server and runs the integration tests.
    """
    
    p = buildAndStartJavaServer()
    try:
        unittest.main()
    finally:
        stopJavaServer(p)
