# -*- coding: utf-8 -*-

'''
torstack.storage.sync_memcache
sync memcache storage definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import memcache

class SyncMemcahhe(object):
    def __init__(self, configs=[], expire=1800, debug=False):
        if not configs:
            raise BaseException('100001', 'error memcache config.')

        self.config_list = []
        self._client = None
        self._expire = expire
        self._debug = debug
        self.init_configs(configs)

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
            raise BaseException('10101', 'error memcache config.')

        for config in configs:
            try:
                host, port, weight = config.get('host'), config.get('port'), config.get('weight')

                if not isinstance(host, str):
                    raise ValueError('Invalid host')
                if not port:
                    port = 11211
                elif not isinstance(port, int):
                    raise ValueError('Invalid port')

                engine_url = '%s:%d' % (host, port)
                self.config_list.append((engine_url, weight))
            except Exception as e:
                raise Exception('error: %s', str(e))

    def _create_client(self):
        '''
        create memcache client
        :return:
        '''
        self._client = memcache.Client(self.config_list, debug=self._debug)

    @property
    def client(self):
        '''
        get redis client
        :return:
        '''
        if not self._client:
            self._create_client()
        return self._client

    def get(self, key):
        '''
        get value of key
        :param key:
        :return:
        '''
        return self.client.get(key)

    def save(self, key, value, lifetime=None):
        '''
        save key value
        :param key:
        :param value:
        :param lifetime:
        :return:
        '''
        self.client.set(key, value)
        if lifetime:
            self.client.expire(key, lifetime)
        return

    def delete(self, key):
        '''
        delete key
        :param key:
        :return:
        '''
        return self.client.expire(key, 0)

    def expire(self, key, lifetime=0):
        '''
        set key expire time
        :param key:
        :param lifetime:
        :return:
        '''
        return self.client.expire(key, lifetime)
