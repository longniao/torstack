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


A Simple Config
---------------

.. code-block:: python

    [application]
    port : 8000
    max_threads_num : 500
    autoreload : True
    settings = {
      'template_path' : 'website/template',
      'static_path' : 'website/static',
      'compress_response' : True,
      'cookie_secret' : '__cookie_secret__',
      'xsrf_cookies' : False,
      'login_url' : '/login',
      'debug' : True,
      'autoreload' : False
      }
    log = {
      'log_level' : 'WARNING',
      'log_console' : False,
      'log_file' : True,
      'log_path' : '/tmp/logs',
      'when' : 'D',
      'interval' : '1',
      'backupCount' : '30'
      }


A Simple Example
----------------

.. code-block:: python

    import os
    from tornado import gen
    from torstack.server import TorStackServer
    from torstack.handler.base import BaseHandler

    class MainHandler(BaseHandler):
        def get(self):
            self.write("Hello, world")

    def main():
        server = TorStackServer()
        server.config.load('./dev.conf')
        server.add_handlers([(r"/", MainHandler)])
        server.run()

    if __name__ == "__main__":
        main()


Features
--------

* session
* cookie
* database
* redis
* taskmgr
* websocket


Python libraries
----------------

* redis
* aioredis
* sqlalchemy
* aiomysql
* asyncpg
* motor
* apscheduler
* elasticsearch


.. _Tornado: http://www.tornadoweb.org
.. _pip: https://pip.pypa.io/en/stable/quickstart/
