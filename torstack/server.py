# -*- coding: utf-8 -*-

'''
torstack.server
server definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import sys
import asyncio
import tornado, tornado.options
import tornado.platform.asyncio
from torstack.config.parser import Parser as ConfigParser
from torstack.app.web import WebApplication
import tornado.locale

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

    def add_smtp(self, config=None):
        '''
        add smtp service
        :return:
        '''
        if not config:
            config = self.application.config['smtp']['smtp']
        from torstack.smtp.listener import SmtpListener
        smtpListener = SmtpListener(config)
        smtpListener.daemon = True
        smtpListener.start()

    def add_service(self, service_name='', service=None):
        '''
        add service to torstack server
        :param service_name:
        :param service:
        :return:
        '''
        if service_name and service:
            setattr(self.application, service_name, service)

    def add_locale(self, locale_path='.', default=None):
        '''
        add locale support
        :param locale_path:
        :param default:
        :return:
        '''
        tornado.locale.load_translations(locale_path)
        if default:
            tornado.locale.set_default_locale(default)

    def run(self, port=None):
        '''
        run with ioloop
        :param port:
        :return:
        '''

        if not port:
            port = self.config._dict['application']['port']

        tornado.options.parse_command_line()
        # application = WebApplication(handlers=self.handlers, config=self.config._dict)
        http_server = tornado.httpserver.HTTPServer(self.application)

        # 判断是否为debug环境
        if self.config._dict['application']['settings']['debug']:
            # debug环境下，单进程模式
            http_server.listen(port)
        else:
            # 加载日志管理
            # CoreLog(options.log)

            # 生产环境下，多进程模式
            http_server.bind(port)
            http_server.start(1)  # Forks multiple sub-processes

        # app.listen(options.port,xheaders=True)
        try:
            print ('Server running on http://localhost:{}'.format(port))
            # ioloop = tornado.ioloop.IOLoop.current()
            ioloop = tornado.ioloop.IOLoop.instance()
            ioloop.start()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        finally:
            tornado.ioloop.IOLoop.instance().stop()


    def run_asyncio(self, port=None):
        '''
        run with asyncio
        :param port:
        :return:
        '''

        if not port:
            port = self.config._dict['application']['port']

        tornado.options.parse_command_line()

        tornado.platform.asyncio.AsyncIOMainLoop().install()

        http_server = tornado.httpserver.HTTPServer(self.application)
        http_server.bind(port)
        http_server.start(1)  # Forks multiple sub-processes

        asyncio.get_event_loop().run_forever()

