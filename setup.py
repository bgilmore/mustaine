import sys
from setuptools import find_packages, setup
from mustaine import __version__

if sys.version_info < (2,6):
    raise NotImplementedError("Sorry, you need at least Python 2.6 to use mustaine")

setup(
    name = "mustaine",
    version = __version__,
    description = "Hessian RPC Library",
    long_description = """\
About
=====

Mustaine is a Python implemention of the `Hessian 1.0.2 specification
<http://hessian.caucho.com/doc/hessian-1.0-spec.xtp>`). Currently, it provides a standard
HTTP-based client as well as a generic (de/)serialization library.

Usage
=====

  from mustaine.client import HessianProxy
  service = HessianProxy("http://hessian.caucho.com/test/test")
  print service.replyDate_1()

Source
======

Up-to-date sources and documentation can always be found at the `mustaine GoogleCode site
<http://code.google.com/p/mustaine/>`_.
    """,

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Object Brokering',
        'Topic :: Software Development :: Libraries',
    ],

    url = "http://code.google.com/p/mustaine",

    maintainer = "Brandon Gilmore",
    maintainer_email = "brandon@mg2.org",
    license = "BSD",

    platforms = "any",
    packages = find_packages(exclude=["test"])
)

