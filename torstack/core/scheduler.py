# -*- coding: utf-8 -*-

'''
torstack.core.scheduler
scheduler.py definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import logging
logger = logging.getLogger(__name__)

DBTYPE_MYSQL = 'mysql'
DBTYPE_MONGO = 'mongodb'

class CoreScheduler(object):
    '''
    docstring for scheduler
    '''
    def __init__(self,schedExecuters,client,dbtype="mysql",dbname='',tablename="scheduler_job"):
        '''
           参数：
               schedExecuters － 执行者列表
               storage        － 数据库连接
               dbname         － 数据库名称
               dbType         － 数据库类型
        '''

        super(CoreScheduler, self).__init__()

        self.executers = dict([ (x.id, x.path) for x in schedExecuters ])

        self.dbClient = client
        self.dbType = dbtype
        self.dbname = dbname

        from apscheduler.schedulers.background import BackgroundScheduler

        self.scheduler = BackgroundScheduler()

        if dbtype == DBTYPE_MYSQL:
            client.use(dbname)
            engine = client.get_engine()
            self.scheduler.add_jobstore('sqlalchemy',tablename=tablename,engine=engine,pickle_protocol=0)

        elif dbtype == DBTYPE_MONGO:
            self.scheduler.add_jobstore('mongodb',database=dbname, collection=tablename,client=client,pickle_protocol=0)


    def start(self):
        self.scheduler.start()