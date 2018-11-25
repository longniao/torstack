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
import tornado.httpserver
import tornado.web
from tornado.options import options
from torstack.config.default import *


class WebApplication(tornado.web.Application):

    settings = {}

    def __init__(self):

        if hasattr(options, '_CONFIG_DICT_'):
            config = options._CONFIG_DICT_
        else:
            raise BaseException('10001', 'error config.')

        # ===================================================================
        # ======= config ====================================================
        # ===================================================================

        # application
        if 'application' not in config:
            raise BaseException('10002', 'error application config.')

        # application settings
        self.settings = application_config.update(config['application'])

        # base
        if 'base' in config:
            self.settings['_config_base'] = base_config.update(config['base'])

        # session config
        if 'session' in config:
            self.settings['_config_session'] = session_config.update(config['session'])

        # cookie config
        if 'cookie' in config:
            self.settings['_config_cookie'] = cookie_config.update(config['cookie'])

        # ===================================================================
        # ======= storage ===================================================
        # ===================================================================

        # redis
        if 'redis' in config:
            from torstack.storage.redis import RedisStorage
            redis_storage = RedisStorage(config['redis'])
            self.settings['_storage_redis'] = redis_storage

        # mysql
        if 'mysql' in config:
            from torstack.storage.mysql import MysqlStorage
            mysql_storage = MysqlStorage(config['mysql'])
            self.settings['_storage_mysql'] = mysql_storage

        # mongodb
        if 'mongodb' in config:
            pass

        # memcache
        if 'memcache' in config:
            pass

        # ===================================================================
        # ======= session and cookie ========================================
        # ===================================================================

        # session
        from torstack.core.session import CoreSession
        self.settings['session'] = CoreSession(redis_storage, self.settings['_config_session'])

        # cookie
        from torstack.core.cookie import CoreCookie
        self.settings['cookie'] = CoreCookie(self.settings['_config_cookie'])


    def run(self, handlers):
        '''
        run application
        :param handlers:
        :return:
        '''
        if not handlers:
            raise BaseException('10003', 'error application handlers.')

        tornado.web.Application.__init__(self, handlers, **self.settings)