# -*- coding: utf-8 -*-

'''
torstack.application.application
Basic application definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import importlib
import sys

importlib.reload(sys)
import tornado.web
from torstack.exception import BaseException

class WebApplication(tornado.web.Application):

    config = None
    session = None
    cookie = None
    storage = dict()
    taskmgr = None
    rest = None

    def __init__(self, handlers=None, config=None):

        self.config = config

        # ===================================================================
        # ======= storage ===================================================
        # ===================================================================

        # mysql
        if config['storage']['mysql_enable'] == True:
            from torstack.storage.mysql import MysqlStorage
            self.storage['mysql'] = MysqlStorage(config['storage']['mysql'])

        # mongodb
        if config['storage']['mongodb_enable'] == True:
            self.storage['mongodb'] = None

        # redis
        if config['storage']['redis_enable'] == True:
            from torstack.storage.redis import RedisStorage
            redis_storage = RedisStorage(config['storage']['redis'])
            self.storage['redis'] = redis_storage

        # memcache
        if config['storage']['memcache_enable'] == True:
            self.storage['memcache'] = None

        # ===================================================================
        # ======= session and cookie ========================================
        # ===================================================================

        # session
        if config['base']['session']['enable'] == True:
            config_session = config['base']['session']
            if config_session['storage'] in self.storage:
                driver = self.storage.get(config_session['storage'])
            else:
                from torstack.storage.file import FileStorage
                config['base']['session']['storage'] = 'file'
                driver = FileStorage()
            from torstack.core.session import CoreSession
            self.session = CoreSession(driver, config_session)

        # cookie
        if config['base']['cookie']['enable'] == True:
            from torstack.core.cookie import CoreCookie
            self.cookie = CoreCookie(config['base']['cookie'])

        # ===================================================================
        # ======= rest ======================================================
        # ===================================================================

        # rest
        if config['rest']['rest']['enable'] == True:
            from torstack.core.rest import CoreRest
            self.rest = CoreRest(redis_storage, config['rest'], config['rest']['rest_header'])

        # ===================================================================
        # ======= websocket =================================================
        # ===================================================================

        # websocket
        if config['websocket']['enable'] == True:
            if 'redis' not in self.storage:
                raise BaseException('10110', 'Redis storage is necessary for websocket')
            from torstack.websocket.listener import ClientListener
            clientListener = ClientListener(self.storage['redis'], config['websocket']['redis_channel'])
            clientListener.daemon = True
            clientListener.start()

        # ===================================================================
        # ======= scheduler =================================================
        # ===================================================================

        if config['scheduler']['scheduler']['enable'] == True:
            config_scheduler = config['scheduler']['scheduler']
            if config_scheduler['dbtype'] in self.storage:
                client = self.storage.get(config_scheduler['dbtype'])
            else:
                raise BaseException('10001', 'error scheduler dbtype config.')

            from torstack.core.scheduler import CoreScheduler
            taskmgr = CoreScheduler(config['scheduler']['scheduler_executers'], client, config['scheduler']['scheduler']['dbtype'], config['scheduler']['scheduler']['dbname'])
            taskmgr.start()

            self.taskmgr = taskmgr

            from torstack.scheduler.handler import scheduler_handlers
            handlers.extend(scheduler_handlers)

        super(WebApplication, self).__init__(handlers=handlers, **config['application']['settings'])


    def run(self):

        # 判断是否为debug环境
        if self.config['application']['settings']['debug']:
            # debug环境下，单进程模式
            self.listen(self.config['application']['port'])
        else:
            # 加载日志管理
            # CoreLog(options.log)

            # 生产环境下，多进程模式
            self.bind(self.config['application']['port'])
            self.start(0)  # Forks multiple sub-processes

        # app.listen(options.port,xheaders=True)
        try:
            print ('Server running on http://localhost:{}'.format(self.config['application']['port']))
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
