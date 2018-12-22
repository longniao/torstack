# -*- coding: utf-8 -*-

'''
torstack.storage.mongodb_async
async mongodb storage definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import motor
from torstack.exception import BaseException

class AsyncMongodb(object):

    def __init__(self, configs=[]):
        if not configs:
            raise BaseException('10102', 'error mongodb config.')

        self.current_db = None
        self.config_list = []
        self.clientPool = {}

        self.init_configs(configs)
        self.init_pool()


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
            engine, session = self.__create_single_client(config)
            self.clientPool[instance].append(engine)

    def __create_single_client(self, config, async=True):
        '''
        create single client
        :param config:
        :param async:
        :return:
        '''
        client_url = 'mongodb://%s:%s@%s:%s/%s' % (config['username'], config['password'], config['host'], config['port'], config['dbname'])
        client = motor.motor_tornado.MotorClient(client_url)
        if async:
            return client.open_sync()
        else:
            return client

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
