# -*- coding: utf-8 -*-

'''
torstack.storage.async_redis
async redis storage definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import tornadoredis

class AsyncRedis(object):

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
            self._pool = tornadoredis.ConnectionPool(host=self.options['host'],port=self.options['port'], password=self.options['password'], db=self.options['db'], max_connections=250, wait_for_available=True)
        return self._pool

    @property
    def client(self):
        '''
        get redis client
        :return:
        '''
        if not self._client:
            self._client = tornadoredis.Client(host=self.options['host'],port=self.options['port'], password=self.options['password'], selected_db=self.options['db'])
        return self._client
