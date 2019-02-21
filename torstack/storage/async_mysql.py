# -*- coding: utf-8 -*-

'''
torstack.storage.sync_mysql
sync mysql storage definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from __future__ import print_function

from torstack.exception import BaseException
import asyncio
import sqlalchemy as sa
from aiomysql.sa import create_engine
from contextlib import contextmanager

engine_setting = dict(
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


class AsyncMysql(object):
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
        self.check_pool()

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
                host, port, dbname, username, password, master = config.get('host'), config.get('port'), config.get(
                    'dbname'), config.get('username'), config.get('password'), config.get('type', 'master')

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
            if config['dbname'] not in self.enginePool:
                self.enginePool[config['dbname'] + '_master'] = []
                self.enginePool[config['dbname'] + '_slave'] = []
                self.sessionPool[config['dbname'] + '_master'] = []
                self.sessionPool[config['dbname'] + '_slave'] = []

    def create_pool(self):
        '''
        create dataqbase instances
        :param hosts:
        :return:
        '''
        for config in self.config_list:
            instance = '%s_%s' % (config['dbname'], config['type'])
            engine, session = self.__create_single_session(config)
            self.enginePool[instance].append(engine)
            self.sessionPool[instance].append(session)

    def check_pool(self):
        '''
        fix pool
        :return:
        '''
        for dbname in self.enginePool:
            if not self.enginePool[dbname]:
                raise ValueError('database [%s] have no instance' % dbname)

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
        engine_url = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (
            config['username'], config['password'], config['host'], config['port'], config['dbname'])
        engine = create_engine(engine_url, **engine_setting)
        return engine

    def close(self, instance):
        '''
        Close an instance
        :param instance:
        :return:
        '''
        pass

    def use(self, dbname, dbtype='master'):
        '''
        set dbname
        :param dbname:
        :return:
        '''
        self.current_db = '%s_%s' % (dbname, dbtype)
        return self

    def get_session(self, dbname=None, dbtype='master'):
        try:
            if not self.current_db:
                if not dbname:
                    raise KeyError('error dbname')
                else:
                    self.use(dbname, dbtype)

            return choice(self.sessionPool[self.current_db])
        except KeyError:
            raise KeyError('{} not created, check your DB_SETTINGS'.format(self.current_db))
        except IndexError:
            raise IndexError('cannot get names from DB_SETTINGS')

    def get_engine(self, dbname=None, dbtype='master'):
        try:
            if not self.current_db:
                if not dbname:
                    raise KeyError('error dbname')
                else:
                    self.use(dbname, dbtype)

            return choice(self.enginePool[self.current_db])
        except KeyError:
            raise KeyError('{} not created, check your DB_SETTINGS'.format(self.current_db))
        except IndexError:
            raise IndexError('cannot get names from DB_SETTINGS')

    @contextmanager
    def session_ctx(self, dbname=None, dbtype='master'):
        DBSession = self.get_session(dbname, dbtype)
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
