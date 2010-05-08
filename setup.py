import sys
from distutils.core import setup

if sys.version_info < (2,6):
    raise NotImplementedError("Sorry, you need at least Python 2.6 to use mustaine")

setup(
    name = "mustaine",
    version = "0.0",
    description = "Hessian RPC Library",
    long_description = "Mustaine is a library providing client and server RPC functionality according to the Hessian specification (http://hessian.caucho.com/doc/)",
    url = "http://code.google.com/p/mustaine",
    license = "BSD",

    platforms = "any",
    py_modules = [ "mustaine" ],
)

