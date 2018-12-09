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

        # application settings
        if 'settings' in config:
            settings_config.update(config['settings'])
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
        self.settings['_scheduler_config'] = scheduler_config

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
            from torstack.storage.redis import RedisStorage
            redis_storage = RedisStorage(config['redis'])
            self.settings['_storage_redis'] = redis_storage

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
            if self.settings['_scheduler_config']['dbtype'] == 'mysql':
                client = self.settings['_storage_mysql']
            elif self.settings['_scheduler_config']['dbtype'] == 'mongodb':
                client = self.settings['_storage_mysql']
            else:
                raise BaseException('10001', 'error scheduler dbtype config.')

            from torstack.core.scheduler import CoreScheduler
            taskmgr = CoreScheduler(self.settings['_scheduler_executers'], client, self.settings['_scheduler_config']['dbtype'], self.settings['_scheduler_config']['dbname'])
            taskmgr.start()
            self.settings['_taskmgr'] = taskmgr

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
            self.settings['_handlers'] = handlers


    def add_handlers(self, handlers):
        '''
        run application
        :param handlers:
        :return:
        '''
        if not handlers:
            raise BaseException('10003', 'error application handlers.')
        self.settings['_handlers'].extend(handlers)


    def ready(self):
        '''
        :return:
        '''
        tornado.web.Application.__init__(self, self.settings['_handlers'], **self.settings)

