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
            from torstack.storage.sync_mysql import SyncMysql
            from torstack.storage.async_mysql import AsyncMysql
            if config['storage']['mysql_drive'] == 'sync':
                self.storage['sync_mysql'] = SyncMysql(config['storage']['mysql'])
            elif config['storage']['mysql_drive'] == 'async':
                self.storage['async_mysql'] = AsyncMysql(config['storage']['mysql'])
            elif config['storage']['mysql_drive'] == 'both':
                self.storage['sync_mysql'] = SyncMysql(config['storage']['mysql'])
                self.storage['async_mysql'] = AsyncMysql(config['storage']['mysql'])
            else:
                raise BaseException('10001', 'error mysql storage config.')

        # mongodb
        if config['storage']['mongodb_enable'] == True:
            from torstack.storage.async_mongodb import AsyncMongodb
            self.storage['mongodb'] = AsyncMongodb(config['storage']['mongodb'])

        # redis
        if config['storage']['redis_enable'] == True:
            from torstack.storage.sync_redis import SyncRedis
            redis_storage = SyncRedis(config['storage']['redis'])
            self.storage['redis'] = redis_storage

        # memcache
        if config['storage']['memcache_enable'] == True:
            from torstack.storage.sync_memcache import SyncMemcahhe
            self.storage['memcache'] = SyncMemcahhe(config['storage']['memcache'])

        # file default
        from torstack.storage.sync_file import SyncFile
        self.storage['file'] = SyncFile()

        # ===================================================================
        # ======= session and cookie ========================================
        # ===================================================================

        # session
        if config['base']['session_enable'] == True:
            config_session = config['base']['session']
            if config_session['storage'] in self.storage:
                driver = self.storage.get(config_session['storage'])
            else:
                raise BaseException('10001', 'error session storage config.')

            from torstack.core.session import CoreSession
            self.session = CoreSession(driver, config_session)

        # cookie
        if config['base']['cookie_enable'] == True:
            from torstack.core.cookie import CoreCookie
            self.cookie = CoreCookie(config['base']['cookie'])

        # ===================================================================
        # ======= rest ======================================================
        # ===================================================================

        # rest
        if config['rest']['rest_enable'] == True:
            config_rest = config['rest']['rest']
            if config_rest['storage'] in self.storage:
                driver = self.storage.get(config_rest['storage'])
            else:
                raise BaseException('10001', 'error rest storage config.')

            from torstack.core.rest import CoreRest
            self.rest = CoreRest(driver, config['rest'])

        # ===================================================================
        # ======= scheduler =================================================
        # ===================================================================

        if config['scheduler']['scheduler_enable'] == True:
            config_scheduler = config['scheduler']['scheduler']
            if config_scheduler['storage'] in self.storage:
                driver = self.storage.get(config_scheduler['storage'])
            else:
                raise BaseException('10001', 'error scheduler storage config.')

            from torstack.core.scheduler import CoreScheduler
            taskmgr = CoreScheduler(config['scheduler']['scheduler_executers'], driver, config_scheduler)
            taskmgr.start()

            self.taskmgr = taskmgr

            from torstack.scheduler.handler import scheduler_handlers
            handlers.extend(scheduler_handlers)

        # ===================================================================
        # ======= elasticsearch =============================================
        # ===================================================================

        if config['elasticsearch']['elasticsearch_enable'] == True:
            from elasticsearch_async import AsyncElasticsearch
            self.elasticsearch = AsyncElasticsearch(**config['elasticsearch']['elasticsearch'])

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
