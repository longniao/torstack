# -*- coding: utf-8 -*-

'''
torstack..server
server definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import tornado
from torstack.config.container import ConfigContainer
from torstack.app.web import WebApplication

class TorStackServer(object):

    def __init__(self):
        pass

    @property
    def config(self):
        '''
        get ConfigContainer
        :return:
        '''
        return ConfigContainer

    def run(self, handlers=[]):
        '''
        run application
        :return:
        '''
        tornado.options.parse_command_line()
        application = WebApplication()
        application.add_handlers(handlers)
        application.ready()
        http_server = tornado.httpserver.HTTPServer(application)

        # 判断是否为debug环境
        if application.settings['debug']:
            # debug环境下，单进程模式
            http_server.listen(application.settings['port'])
        else:
            # 加载日志管理
            # CoreLog(options.log)

            # 生产环境下，多进程模式
            http_server.bind(application.settings['port'])
            http_server.start(0)  # Forks multiple sub-processes

        # app.listen(options.port,xheaders=True)
        try:
            # ioloop = tornado.ioloop.IOLoop.current()
            ioloop = tornado.ioloop.IOLoop.instance()

            # websocket 定时广播
            # from interest.repository.package.websocket_service import *
            # loop.spawn_callback(minute_loop2)

            ioloop.start()
            print ('Server running on http://localhost:{}'.format(application.settings['port']))

        except KeyboardInterrupt:
            tornado.ioloop.IOLoop.instance().stop()






