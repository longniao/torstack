# -*- coding: utf-8 -*-

'''
torstack.core.scheduler
scheduler.py definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import logging
logger = logging.getLogger(__name__)

DBTYPE_MYSQL = 'sync_mysql'
DBTYPE_MONGO = 'mongodb'

class CoreScheduler(object):
    '''
    docstring for scheduler
    '''
    def __init__(self, schedExecuters, driver, config_scheduler):
        '''
        CoreScheduler
        :param schedExecuters:
        :param driver:
        :param config_scheduler:
        '''
        super(CoreScheduler, self).__init__()

        self.executers = dict([ (x.id, x.path) for x in schedExecuters ])

        self.driver = driver
        self.storage = config_scheduler.get('storage', 'sync_mysql')
        self.dbname = config_scheduler.get('dbname', 'test')
        self.tablename = config_scheduler.get('tablename', 'scheduler_job')

        from apscheduler.schedulers.background import BackgroundScheduler

        self.scheduler = BackgroundScheduler()

        if self.storage == DBTYPE_MYSQL:
            self.driver.use(self.dbname)
            engine = self.driver.get_engine()
            self.scheduler.add_jobstore('sqlalchemy', tablename=self.tablename, engine=engine, pickle_protocol=0)

        elif storage == DBTYPE_MONGO:
            self.scheduler.add_jobstore('mongodb', database=self.dbname, collection=self.tablename, client=self.driver, pickle_protocol=0)


    def start(self):
        self.scheduler.start()