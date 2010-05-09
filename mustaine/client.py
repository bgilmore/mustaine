#!/usr/bin/env python

class HessianProxy(object):
    
    """HTTP Hessian RPC Client
    
    Implements Hessian 2.0 spec RPC against HTTP(S) web services
    """
    
    def __init__(self, service_uri, credentials=None):
        """Creates a Client Proxy for the given URL
        
        Args:
          service_uri: HTTP URI for the Hessian service
          credentials: (optional) a tuple of username,password to be used for HTTP Basic Auth
        """
        self._uri = service_uri
        
        if credentials:
            pass # TODO: set up BasicAuthProvider
    
    class __AutoMethod(object):
        # provides dark magic for autoloading methods
        def __init__(self, caller, method):
            self.__caller = caller
            self.__method = method
        def __call__(self, *args):
            self.__caller(self.__method, args)    
    
    def __getattr__(self, method):
        return self.__AutoMethod(self, method)
    
    def __call__(self, method, args):
        print "Method=%r, Args=%r" % (method,args,)
        
    
