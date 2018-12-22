# -*- coding: utf-8 -*-

'''
torstack.storage.async_redis
async redis storage definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import redis

class SyncRedis(object):
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
        get redis pool
        :return:
        '''
        if not self._pool:
            self._pool = redis.ConnectionPool(host=self.options['host'],port=self.options['port'], password=self.options['password'], db=self.options['db'])
        return self._pool

    @property
    def client(self):
        '''
        get redis client
        :return:
        '''
        if not self._client:
            self._client = redis.StrictRedis(connection_pool=self.pool, charset="utf-8", decode_responses=True)
        return self._client

    @property
    def pipeline(self):
        '''
        get redis pipeline
        :return:
        '''
        return self.client.pipeline()

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

    def publish(self, channel, message):
        '''
        redis publish
        :param channel:
        :param message:
        :return:
        '''
        return self.client.publish(channel, message)
