About
-----

Mustaine is a Python implemention of the `Hessian 1.0.2 specification
<http://hessian.caucho.com/doc/hessian-1.0-spec.xtp>`_, a binary web services
protocol. The library currently provides a standard HTTP-based client as well
as a general-purpose serialization library. Server support is planned.

Usage
-----

Using `mustaine.client`
+++++++++++++++++++++++

Testing against `Caucho <http://hessian.caucho.com/>`_'s reference service::

  from mustaine.client import HessianProxy
  service = HessianProxy("http://hessian.caucho.com/test/test")
  print service.replyDate_1()

Source
------

Up-to-date sources and documentation can always be found at the `mustaine
GitHub site <http://github.com/bgilmore/mustaine>`_.
