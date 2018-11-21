Torstack
========

.. image:: ./docs/logo.svg
  :width: 300px

Torstack is a full stack framework base on `Tornado`_. it is designed to make getting started quick and easy, so you can focus on writing your app without needing to reinvent the wheel.


Installing
----------

Install and update using `pip`_:

.. code-block:: text

    pip install -U torstack


A Simple Demo
-------------

.. code-block:: python

    from torstack import Application

    if __name__ == "__main__":
        app = Application()
        app.listen(8888)
        app.run()

Features
--------

* to be continued


.. _Tornado: http://www.tornadoweb.org
.. _pip: https://pip.pypa.io/en/stable/quickstart/