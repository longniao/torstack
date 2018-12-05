# -*- coding: utf-8 -*-

'''
torstack.storage.redis
redis storage definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import redis

class RedisStorage(object):
    def __init__(self, options):
        if not options:
            raise BaseException('100001', 'error redis config.')

        self.options = options
        self._pool = None
        self._client = None
        self._expire = 1800


    @property
    def pool(self):
        '''
        连接池
        :return:
        '''
        if not self._pool:
            self._pool = redis.ConnectionPool(host=self.options['host'],port=self.options['port'], password=self.options['password'], db=self.options['db'])
        return self._pool

    @property
    def client(self):
        '''
        客户端
        :return:
        '''
        if not self._client:
            self._client = redis.StrictRedis(connection_pool=self.pool, charset="utf-8", decode_responses=True)
        return self._client

    @property
    def pipeline(self):
        '''
        管道
        :return:
        '''
        return self.client.pipeline()

    def get(self, key):
        return self.client.get(key)

    def save(self, key, value, lifetime=None):
        self.client.set(key, value)
        if lifetime:
            self.client.expire(key, lifetime)
        return

