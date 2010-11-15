import os, sys
from setuptools import find_packages, setup, Extension, Feature
from mustaine import __version__

if sys.version_info < (2,6):
    raise NotImplementedError("mustaine requires Python 2.6 or later")

src_root = os.path.dirname(__file__)

speedups = Feature(
    description = "C extension providing speed improvements",
    standard = True,
    optional = True,

    ext_modules = [
        Extension(
            "mustaine._speedups",
            sources = [os.path.join(src_root, "ext", "speedups.c")],
        )
    ]
)

setup(
    name = "mustaine",
    version = __version__,
    description = "Hessian RPC Library",
    long_description = file(os.path.join(src_root, "README.rst")).read(),

    features = {
        "speedups": speedups,
    },

    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Object Brokering",
        "Topic :: Software Development :: Libraries",
    ],

    url = "http://github.com/bgilmore/mustaine",

    author = "Brandon Gilmore",
    author_email = "brandon@mg2.org",
    license = "BSD",

    platforms = "any",
    packages = find_packages(exclude=["test"]),
    zip_safe = True,
)

