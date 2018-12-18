# -*- coding: utf-8 -*-

'''
torstack.server
server definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import tornado
import asyncio
from torstack.config.parser import Parser as ConfigParser
from torstack.app.web import WebApplication
from threading import Thread

class DefaultHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello TorStack!")

class TorStackServer(object):
    '''
    torstack webserver
    '''

    config = ConfigParser()
    handlers = [(r'/', DefaultHandler),]
    executers = []
    application = None

    def __init__(self):
        pass

    def add_handlers(self, handlers=None):
        '''
        load handlers
        :param handlers:
        :return:
        '''
        if handlers:
            self.handlers = handlers

    def add_executers(self, executers=[]):
        '''
        add executers
        :param executers:
        :return:
        '''
        if executers:
            self.config._dict['scheduler']['scheduler_executers'].extend(executers)

    def init_application(self):
        '''
        init application
        :return:
        '''
        self.application = WebApplication(handlers=self.handlers, config=self.config._dict)

    def start_server(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.application.run()

    def run(self):
        '''
        run application
        :return:
        '''
        self.init_application()
        t = Thread(target=self.start_server(), args=())
        t.daemon = True
        t.start()
        t.join()






