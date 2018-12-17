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
from torstack.exception import BaseException
import tornado.web
from tornado.options import options
from torstack.config.default import *

class WebApplication(tornado.web.Application):

    settings = {}

    def __init__(self, handlers=None, **settings):

        if hasattr(options, '_CONFIG_DICT_'):
            config = options._CONFIG_DICT_
        else:
            raise BaseException('10001', 'error config.')

        # ===================================================================
        # ======= config ====================================================
        # ===================================================================

        # application settings
        if 'settings' in config:
            settings_config.update(config['settings'])

        if settings and isinstance(settings, dict):
            settings_config.update(settings)

        self.settings = settings_config

        # application log
        if 'log' in config:
            log_config.update(config['log'])
        self.settings['_config_log'] = log_config

        # session config
        if 'session' in config:
            session_config.update(config['session'])
        self.settings['_config_session'] = session_config

        # cookie config
        if 'cookie' in config:
            cookie_config.update(config['cookie'])
        self.settings['_config_cookie'] = cookie_config

        # rest config
        if 'rest' in config:
            rest_config.update(config['rest'])
        self.settings['_config_rest'] = rest_config

        if 'rest_header' in config:
            rest_header_config.update(config['rest_header'])
        self.settings['_config_rest_header'] = rest_header_config

        # websocket config
        if 'websocket' in config:
            websocket_config.update(config['websocket'])
        self.settings['_config_websocket'] = websocket_config

        # scheduler config
        if 'scheduler' in config:
            scheduler_config.update(config['scheduler'])
        self.settings['_config_scheduler'] = scheduler_config

        # scheduler executers
        if 'executers' in config:
            scheduler_executers.extend(config['executers'])
        self.settings['_scheduler_executers'] = scheduler_executers
        self.settings['_handlers'] = []

        # ===================================================================
        # ======= storage ===================================================
        # ===================================================================

        # mysql
        if 'mysql' in config:
            from torstack.storage.mysql import MysqlStorage
            self.settings['_storage_mysql'] = MysqlStorage(config['mysql'])

        # mongodb
        if 'mongodb' in config:
            pass

        # ===================================================================
        # ======= cache =====================================================
        # ===================================================================

        # redis
        if 'redis' in config:
            self.settings['_config_redis'] = config['redis']

            from torstack.storage.redis import RedisStorage
            redis_storage = RedisStorage(self.settings['_config_redis'])
            self.settings['_storage_redis'] = redis_storage

        # memcache
        if 'memcache' in config:
            self.settings['_config_memcache'] = config['memcache']
            pass

        # ===================================================================
        # ======= session and cookie ========================================
        # ===================================================================

        # session
        if self.settings['_config_session']['enable'] == True:
            from torstack.core.session import CoreSession
            self.settings['session'] = CoreSession(redis_storage, self.settings['_config_session'])

        # cookie
        if self.settings['_config_cookie']['enable'] == True:
            from torstack.core.cookie import CoreCookie
            self.settings['cookie'] = CoreCookie(self.settings['_config_cookie'])

        # ===================================================================
        # ======= rest ======================================================
        # ===================================================================

        # rest
        if self.settings['_config_rest']['enable'] == True:
            from torstack.core.rest import CoreRest
            self.settings['rest'] = CoreRest(redis_storage, self.settings['_config_rest'], self.settings['_config_rest_header'])

        # ===================================================================
        # ======= websocket =================================================
        # ===================================================================

        # websocket
        if self.settings['_config_websocket']['enable'] == True:
            from torstack.websocket.listener import ClientListener
            clientListener = ClientListener(redis_storage.client, [self.settings['_config_redis']['channel']])
            clientListener.daemon = True
            clientListener.start()

        # ===================================================================
        # ======= scheduler =================================================
        # ===================================================================

        if self.settings['_config_scheduler']['enable'] == True:
            if self.settings['_config_scheduler']['dbtype'] == 'mysql':
                client = self.settings['_storage_mysql']
            elif self.settings['_config_scheduler']['dbtype'] == 'mongodb':
                client = self.settings['_storage_mysql']
            else:
                raise BaseException('10001', 'error scheduler dbtype config.')

            from torstack.core.scheduler import CoreScheduler
            taskmgr = CoreScheduler(self.settings['_scheduler_executers'], client, self.settings['_config_scheduler']['dbtype'], self.settings['_config_scheduler']['dbname'])
            taskmgr.start()
            self.settings['_taskmgr'] = taskmgr

            from torstack.scheduler.handler import handlers
            self.settings['_handlers'] = handlers

        self.settings['_handlers'].extend(handlers)

        super(WebApplication, self).__init__(handlers=self.settings['_handlers'], **self.settings)


    def run(self):

        # 判断是否为debug环境
        if self.settings['debug']:
            # debug环境下，单进程模式
            self.listen(self.settings['port'])
        else:
            # 加载日志管理
            # CoreLog(options.log)

            # 生产环境下，多进程模式
            self.bind(self.settings['port'])
            self.start(0)  # Forks multiple sub-processes

        # app.listen(options.port,xheaders=True)
        try:
            print ('Server running on http://localhost:{}'.format(self.settings['port']))
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
