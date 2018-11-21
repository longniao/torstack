# -*- coding: utf-8 -*-

'''
torstack.storage.mysql
Basic mysql storage definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from __future__ import print_function

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

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

    def __init__(self, master, slave=None):
        if not master:
            raise Exception('100001', 'Mysql config error.')

        self.session_map = {}
        self.create_sessions()

    def create_sessions(self):
        if self.options:
            for key, value in self.options.items():
                engine_url = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % (value['username'], value['password'], value['host'], value['port'], value['dbname'])
                # print(key, engine_url)
                self.session_map[key] = self.create_single_session(engine_url)

    @classmethod
    def create_single_session(cls, url, scopefunc=None):
        engine = create_engine(url, **engine_setting)
        return scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=True,
                expire_on_commit=False,
                bind=engine
            ),
            scopefunc=scopefunc
        )

    def get_session(self, name):
        try:
            if not name:
                name = 'slave'

            return self.session_map[name]
        except KeyError:
            raise KeyError('{} not created, check your DB_SETTINGS'.format(name))
        except IndexError:
            raise IndexError('cannot get names from DB_SETTINGS')

    @contextmanager
    def session_ctx(self, bind=None):
        DBSession = self.get_session(bind)
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