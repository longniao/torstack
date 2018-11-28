Torstack
========

.. image:: https://travis-ci.org/longniao/torstack.svg
    :target: https://travis-ci.org/longniao/torstack
    :alt: Travis CI

.. image:: https://img.shields.io/pypi/v/torstack.svg
    :target: https://pypi.python.org/pypi/torstack/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/wheel/torstack.svg
    :target: https://pypi.python.org/pypi/torstack/

.. image:: https://img.shields.io/pypi/pyversions/torstack.svg
    :target: https://pypi.python.org/pypi/torstack/

.. image:: https://img.shields.io/pypi/l/torstack.svg
    :target: https://pypi.python.org/pypi/torstack/


Torstack is a bundle for `Tornado`_. it is designed to make getting started quick and easy, so you can focus on writing your app without needing to reinvent the wheel.


Installing
----------

Install and update using `pip`_:

.. code-block:: text

    pip install -U torstack


A Simple Demo
-------------

.. code-block:: python

    from torstack.application import WebApplication

    if __name__ == "__main__":
        app = WebApplication()
        app.listen(8888)
        app.run()

Features
--------

* to be continued


.. _Tornado: http://www.tornadoweb.org
.. _pip: https://pip.pypa.io/en/stable/quickstart/
