# -*- coding: utf-8 -*-

'''
torstack.storage.mongodb_async
async mongodb storage definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import motor
from torstack.exception import BaseException
from contextlib import contextmanager
from random import choice

class AsyncMongodb(object):

    def __init__(self, configs=[]):
        if not configs:
            raise BaseException('10102', 'error mongodb config.')

        self.current_db = None
        self.config_list = []
        self.clientPool = {}

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
            raise BaseException('10102', 'error mongodb config.')

        for config in configs:
            try:
                host, port, dbname, username, password, master = config.get('host'), config.get('port'), config.get('dbname'), config.get('username'), config.get('password'), config.get('type', 'master')

                if not isinstance(host, str):
                    raise ValueError('Invalid host')
                if not port:
                    config['port'] = 27017
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
            if config['dbname'] not in self.clientPool:
                self.clientPool[config['dbname']+'_master'] = []
                self.clientPool[config['dbname']+'_slave'] = []

    def create_pool(self):
        '''
        create dataqbase instances
        :param hosts:
        :return:
        '''
        for config in self.config_list:
            instance = '%s_%s' % (config['dbname'], config['type'])
            client = self.__create_single_client(config)
            self.clientPool[instance].append(client)

    def check_pool(self):
        '''
        fix pool
        :return:
        '''
        for dbname in self.clientPool:
            if not self.clientPool[dbname]:
                raise ValueError('database [%s] have no instance' % dbname)

    def __create_single_client(self, config):
        '''
        create single client
        :param config:
        :param async:
        :return:
        '''
        if not config['username']:
            client_url = 'mongodb://%s:%s' % (config['host'], config['port'])
        else:
            client_url = 'mongodb://%s:%s@%s:%s' % (config['username'], config['password'], config['host'], config['port'])
        if config['dbname']:
            return motor.motor_tornado.MotorClient(client_url)[config['dbname']]
        else:
            return motor.motor_tornado.MotorClient(client_url)

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

            return choice(self.clientPool[self.current_db])
        except KeyError:
            raise KeyError('{} not created, check your DB_SETTINGS'.format(self.current_db))
        except IndexError:
            raise IndexError('cannot get names from DB_SETTINGS')

    @contextmanager
    def session_ctx(self, dbname=None, dbtype='master'):
        session = self.get_session(dbname, dbtype)
        try:
            yield session
        except:
            session.rollback()
            raise
        finally:
            pass
