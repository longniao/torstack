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
from tornado.web import url
from torstack.scheduler.handler import *


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
        application_config.update(config['application'])
        self.settings = application_config

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

        # websocket config
        if 'websocket' in config:
            websocket_config.update(config['websocket'])
        self.settings['_config_websocket'] = websocket_config

        # scheduler config
        if 'scheduler' in config:
            scheduler_config.update(config['scheduler'])
        self.settings['_scheduler_config'] = scheduler_config

        # scheduler config
        if 'executors' in config:
            scheduler_executors.update(config['executors'])
        self.settings['_scheduler_executors'] = scheduler_executors
        self.settings['_scheduler_handlers'] = []

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
            if 'master' in config['mysql']:
                # master and slave
                if 'slave' not in config['mysql']:
                    config['mysql']['slave'] = None
                mysql_storage = MysqlStorage(config['mysql']['master'], config['mysql']['slave'])
            else:
                # only one database
                mysql_config.update(config['mysql'])
                mysql_storage = MysqlStorage(mysql_config, None)
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
            from torstack.websocket.client import ClientListener
            client = ClientListener(redis_storage.client, [options.redis_channel])
            client.start()

        # ===================================================================
        # ======= scheduler =================================================
        # ===================================================================

        if self.settings['_scheduler_config']['enable'] == True:
            from torstack.core.scheduler import CoreScheduler
            taskmgr = CoreScheduler(self.settings['_scheduler_executors'], self.settings['_storage_mysql'])
            taskmgr.start()

            handlers = [
                # 任务
                url(r"/scheduler/job_add", AddJobHandler, name='job_add'),
                url(r"/scheduler/job_pause", PauseJobHandler, name='job_pause'),
                url(r"/scheduler/job_resume", ResumeJobHandler, name='job_resume'),
                url(r"/scheduler/job_remove", RemoveJobHandler, name='job_remove'),
                url(r"/scheduler/job_remove_all", RemoveAllJobsHandler, name='job_remove_all'),
                url(r"/scheduler/job_list", GetAllJobsHandler, name='job_list'),
                # 定时器
                url(r"/scheduler/start", StartHandler, name='scheduler_start'),
                url(r"/scheduler/shutdown", ShutdownSchedHandler, name='scheduler_shutdown'),
                url(r"/scheduler/pause", PauseSchedHandler, name='scheduler_pause'),
                url(r"/scheduler/resume", ResumeSchedHandler, name='scheduler_resume'),
                url(r"/scheduler/status", GetStatusHandler, name='scheduler_status'),
                url(r"/scheduler/switch", SwitchSchedHandler, name='scheduler_switch'),
            ]
            self.settings['_scheduler_handlers'] = handlers


    def add_handlers(self, handlers):
        '''
        run application
        :param handlers:
        :return:
        '''
        if not handlers:
            raise BaseException('10003', 'error application handlers.')
        self.settings['_scheduler_handlers'].extend(handlers)


    def ready(self):
        '''
        :return:
        '''
        tornado.web.Application.__init__(self, self.settings['_scheduler_handlers'], **self.settings)

