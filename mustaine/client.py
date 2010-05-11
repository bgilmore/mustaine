from httplib import HTTPConnection, HTTPSConnection
from urlparse import urlparse
import base64

from mustaine.encoder import encode_object
from mustaine.protocol import HessianCall
import __version__


class ProtocolError(Exception):
    """ Raised when an HTTP error occurs """
    def __init__(self, url, status, reason):
        self._url    = url
        self._status = status
        self._reason = reason
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return "<ProtocolError for {0}: {1} {2}>".format(self._url, self._status, self._reason)


class HessianProxy(object):
    _headers = [
                ('User-Agent', 'mustaine/' + __version__.VERSION_STRING),
                ('Content-Type', 'application/x-hessian'),
               ]

    def __init__(self, service_uri, credentials=None, key_file=None, cert_file=None, timeout=10):
        self._uri = urlparse(service_uri)

        if self._uri.scheme == 'http':
            self._client = HTTPConnection(self._uri.hostname,
                                          self._uri.port or 80,
                                          strict=True,
                                          timeout=timeout)
        elif self._uri.scheme == 'https':
            self._client = HTTPSConnection(self._uri.hostname,
                                           self._uri.port or 443,
                                           key_file=key_file,
                                           cert_file=cert_file,
                                           strict=True,
                                           timeout=timeout)
        else:
            raise NotImplementedError("HessianProxy only supports http:// and https:// URIs")
        
        # autofill credentials if they were passed via url instead of kwargs
        if (self._uri.username and self._uri.password) and not credentials:
            credentials = (self._uri.username, self._uri.password)
        
        if credentials:
            auth = 'Basic ' + base64.b64encode(':'.join(credentials))
            self._headers.append(('Authorization', auth))
    
    
    class __AutoMethod(object):
        # dark magic for autoloading methods
        def __init__(self, caller, method):
            self.__caller = caller
            self.__method = method
        def __call__(self, *args):
            return self.__caller(self.__method, args)
    
    def __getattr__(self, method):
        return self.__AutoMethod(self, method)
    
    def __repr__(self):
        return "<mustaine.client.HessianProxy(\"{url}\")>".format(url=self._uri.geturl())
    
    def __str__(self):
        return self.__repr__()
    
    def __call__(self, method, args):
        self._client.putrequest('POST', self._uri.path)
        for header in self._headers:
            self._client.putheader(*header)
        
        request = encode_object(HessianCall(method, args))

        def hexdump(src, length=8):
            result = []
            digits = 4 if isinstance(src, unicode) else 2
            for i in xrange(0, len(src), length):
               s = src[i:i+length]
               hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
               text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
               result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )
            return b'\n'.join(result)
        print hexdump(request)


        self._client.putheader("Content-Length", str(len(request)))
        self._client.endheaders()
        self._client.send(str(request))
        
        response = self._client.getresponse()
        if response.status != 200:
            raise ProtocolError(self._uri.geturl(), response.status, response.reason)
        
        return response.read()

