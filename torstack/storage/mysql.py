# -*- coding: utf-8 -*-

'''
torstack.storage.mysql
mysql storage definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from __future__ import print_function

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from torstack.exception import BaseException
from random import choice

engine_setting=dict(
        echo=False,  # print sql
        echo_pool=False,
        # 设置7*60*60秒后回收连接池，默认-1，从不重置
        # 该参数会在每个session调用执行sql前校验当前时间与上一次连接时间间隔是否超过pool_recycle，如果超过就会重置。
        # 这里设置7小时是为了避免mysql默认会断开超过8小时未活跃过的连接，避免"MySQL server has gone away”错误
        # 如果mysql重启或断开过连接，那么依然会在第一次时报"MySQL server has gone away"，
        # 假如需要非常严格的mysql断线重连策略，可以设置心跳。
        # 心跳设置参考https://stackoverflow.com/questions/18054224/python-sqlalchemy-mysql-server-has-gone-away
        pool_recycle=25200,
        pool_size=20,
        max_overflow=20,
    )

class MysqlStorage(object):

    def __init__(self, configs=[]):
        if not configs:
            raise BaseException('10101', 'error mysql config.')

        self.current_db = None
        self.config_list = []
        self.enginePool = {}
        self.sessionPool = {}

        self.init_configs(configs)
        self.init_pool()
        self.create_pool()
        self.fix_pool()

    def init_configs(self, configs=[]):
        '''
        Init configurations.
        :param self:
        :param config:
        :return:
        '''
        if isinstance(configs, list):
            pass
        elif isinstance(configs, dict):
            configs = [configs]
        else:
            raise BaseException('10101', 'error mysql config.')

        for config in configs:
            try:
                host, port, dbname, username, password, master = config.get('host'), config.get('port'), config.get('dbname'), config.get('username'), config.get('password'), config.get('type', 'master')

                if not isinstance(host, str):
                    raise ValueError('Invalid host')
                if not port:
                    config['port'] = port = 3306
                elif not isinstance(port, int):
                    raise ValueError('Invalid port')

                self.config_list.append(config)
            except Exception as e:
                raise Exception('error: %s', str(e))

    def init_pool(self):
        '''
        init pool
        :return:
        '''
        for config in self.config_list:
            dbname = config['dbname']
            if dbname not in self.enginePool:
                self.enginePool[dbname] = dict(
                    master=[],
                    slave=[],
                )
                self.sessionPool[dbname] = dict(
                    master=[],
                    slave=[],
                )

    def create_pool(self):
        '''
        create dataqbase instances
        :param hosts:
        :return:
        '''
        for config in self.config_list:
            dbname = config['dbname']
            type = config['type']

            engine, session = self.__create_single_session(config)
            self.enginePool[dbname][type].append(session)
            self.sessionPool[dbname][type].append(session)

    def fix_pool(self):
        '''
        fix pool
        :return:
        '''
        for dbname in self.enginePool:
            pool = self.enginePool[dbname]
            if not pool['master']:
                raise ValueError('database [%s] have no master instance' % dbname)

            if not pool['slave']:
                m = pool['master'][0]
                self.enginePool[dbname]['slave'].append(m)


    def __create_single_session(self, config, scopefunc=None):
        engine = self.__create_single_engine(config)
        return engine, scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=True,
                expire_on_commit=False,
                bind=engine
            ),
            scopefunc=scopefunc
        )

    def __create_single_engine(self, config):
        engine_url = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % (config['username'], config['password'], config['host'], config['port'], config['dbname'])
        engine = create_engine(engine_url, **engine_setting)
        return engine


    def close(self, instance):
        '''
        Close an instance
        :param instance:
        :return:
        '''
        pass


    def get_pool(self, bind, type='session'):
        try:
            if not self.current_db:
                dbs = list(self.sessionPool.keys())
                self.current_db = dbs[0]
            if not bind:
                bind = 'master'

            if type == 'session':
                pool = self.sessionPool
            elif type == 'engine':
                pool = self.enginePool
            else:
                raise KeyError('error pool type')

            if isinstance(pool[self.current_db][bind], list):
                return choice(pool[self.current_db][bind])
            else:
                return pool[self.current_db][bind]
        except KeyError:
            raise KeyError('{} not created, check your DB_SETTINGS'.format(self.current_db))
        except IndexError:
            raise IndexError('cannot get names from DB_SETTINGS')


    def use(self, dbname):
        '''
        set dbname
        :param dbname:
        :return:
        '''
        self.current_db = dbname

    def get_engine(self, bind='master'):
        '''
        get engine
        :return:
        '''
        return self.get_pool(bind, type='engine')

    @contextmanager
    def session_ctx(self, bind='master'):
        DBSession = self.get_pool(bind)
        session = DBSession()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.expunge_all()
            session.close()