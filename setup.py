import sys
from distutils.core import setup
from mustaine import __version__

if sys.version_info < (2,6):
    raise NotImplementedError("Sorry, you need at least Python 2.6 to use mustaine")

setup(
    name = "mustaine",
    version = __version__,
    description = "Hessian RPC Library",
    long_description = "Mustaine is a library providing client and server RPC functionality according to the Hessian specification (http://hessian.caucho.com/doc/)",
    url = "http://code.google.com/p/mustaine",

    maintainer = "Brandon Gilmore",
    maintainer_email = "brandon@mg2.org",
    license = "BSD",

    platforms = "any",
    packages = [ "mustaine" ],
)

