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
            base_config.update(config['base'])
        self.settings['_config_base'] = base_config

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
        if self.settings['_config_session']['enable'] == True:
            from torstack.core.session import CoreSession
            self.settings['session'] = CoreSession(redis_storage, self.settings['_config_session'])

        # cookie
        if self.settings['_config_cookie']['enable'] == True:
            from torstack.core.cookie import CoreCookie
            self.settings['cookie'] = CoreCookie(self.settings['_config_cookie'])

        # ===================================================================
        # ======= rest config ===============================================
        # ===================================================================

        # rest
        if rest_config['_config_rest']['enable'] == True:
            from torstack.core.rest import CoreRest
            self.settings['rest'] = CoreRest(redis_storage, self.settings['_config_rest'], self.settings['_config_rest_header'])


    def run(self, handlers):
        '''
        run application
        :param handlers:
        :return:
        '''
        if not handlers:
            raise BaseException('10003', 'error application handlers.')

        tornado.web.Application.__init__(self, handlers, **self.settings)