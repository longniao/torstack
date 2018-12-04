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
-------------

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

    [base]
    session = {
      'enable' : True,
      'prefix' : 'sid_',
      'lifetime' : 1800,
      }
    cookie = {
      'enable' : True,
      'name' : '_tsid',
      'expires' : 88473600,
      }

    [rest]
    rest = {
      'enable' : False,
      'allow_remote_access' : False,
      'token_prefix' : 'token_',
      'token_lifetime' : 315360000,
      }
    rest_header = {
      'token' : '',
      'version' : '',
      'signature' : '',
      'timestamp' : '',
      }

    [websocket]
    websocket = {
      'enable' : False,
      }

    [scheduler]
    scheduler = {
      'enable' : False,
      'autorun' : False,
      }

    [mysql]
    master = {
      'host' : '127.0.0.1',
      'port' : 3306,
      'dbname' : 'test',
      'username' : '',
      'password' : ''
      }

    [cache]
    redis = {
      'host' : '127.0.0.1',
      'port' : 6379,
      'db' : 2,
      'channel' : 'channel',
      'user' : '',
      'password' : None
      }


A Simple Example
-------------

.. code-block:: python

    import os
    from os.path import abspath, dirname
    from torstack.config.container import ConfigContainer
    from torstack.server import TorStackServer
    from torstack.handler.base import BaseHandler

    PROJECT_DIR = dirname(dirname(abspath(__file__)))
    CONF_DIR = os.path.join(PROJECT_DIR, 'conf')
    CONF_FILE = CONF_DIR + os.path.sep + 'dev.conf'

    ConfigContainer.load_config(CONF_FILE)
    ConfigContainer.store()

    class MainHandler(BaseHandler):
        def get(self):
            self.write("Hello, world")

    def main():
        server = TorStackServer()
        server.run([(r"/", MainHandler)])

    if __name__ == "__main__":
        main()


Features
--------

* to be continued


.. _Tornado: http://www.tornadoweb.org
.. _pip: https://pip.pypa.io/en/stable/quickstart/
