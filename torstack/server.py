# -*- coding: utf-8 -*-

'''
torstack.server
server definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import tornado, tornado.options
from torstack.config.parser import Parser as ConfigParser
from torstack.app.web import WebApplication

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

    def add_websocket(self, channel=None):
        '''
        add websocket service
        :param channel:
        :return:
        '''
        if 'redis' not in self.application.storage:
            raise BaseException('10110', 'Redis storage is necessary for websocket')
        if not channel:
            channel = 'websocket'
        from torstack.websocket.listener import ClientListener
        clientListener = ClientListener(self.application.storage['redis'], channel)
        clientListener.daemon = True
        clientListener.start()

    def run(self):

        tornado.options.parse_command_line()
        # application = WebApplication(handlers=self.handlers, config=self.config._dict)
        http_server = tornado.httpserver.HTTPServer(self.application)

        # 判断是否为debug环境
        if self.config._dict['application']['settings']['debug']:
            # debug环境下，单进程模式
            http_server.listen(self.config._dict['application']['port'])
        else:
            # 加载日志管理
            # CoreLog(options.log)

            # 生产环境下，多进程模式
            http_server.bind(self.config._dict['application']['port'])
            http_server.start(0)  # Forks multiple sub-processes

        # app.listen(options.port,xheaders=True)
        try:
            print ('Server running on http://localhost:{}'.format(self.config._dict['application']['port']))
            # ioloop = tornado.ioloop.IOLoop.current()
            ioloop = tornado.ioloop.IOLoop.instance()

            # websocket 定时广播
            # from interest.repository.package.websocket_service import *
            # loop.spawn_callback(minute_loop2)

            ioloop.start()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        finally:
            tornado.ioloop.IOLoop.instance().stop()


