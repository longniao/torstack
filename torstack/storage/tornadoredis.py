# -*- coding: utf-8 -*-

'''
torstack.storage.tornadoredis
tornadoredis definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import tornadoredis

class TornadoRedisStorage(threading.Thread):

    def __init__(self, options):
        if not options:
            raise BaseException('100001', 'error redis config.')

        self.options = options
        self._pool = None
        self._client = None
        self._expire = 1800

    def __init__(self, pubsub_channel, redis_hostname, redis_port, redis_db, redis_password=None):
        threading.Thread.__init__(self)
        self.pubsub_channel = pubsub_channel
        self.redis_hostname = redis_hostname
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.redis_password = redis_password
        self.subscriptions = collections.defaultdict(collections.deque)
        self._init_redis()

    @property
    def pool(self):
        '''
        get redis pool
        :return:
        '''
        if not self._pool:
            self._pool = tornadoredis.ConnectionPool(host=self.options['host'],port=self.options['port'], password=self.options['password'], db=self.options['db'])
        return self._pool


    def _init_redis(self):
        self.client = self.get_redis_connection()
        self.pubsub = self.client.pubsub()
        self.pubsub.subscribe(self.pubsub_channel)

    def get_redis_connection(self):
        return redis.Redis(
            self.redis_hostname,
            self.redis_port,
            self.redis_db,
            self.redis_password
        )

    def subscribe(self, channel, callback):
        self.subscriptions[channel].append(callback)

    def decode_message(self, message):
        return json.loads(message)

    def parse_message(self, message):
        msg = self.decode_message(message['data'])
        return msg['channel'], msg['data']

    def notify(self, channel, data):
        while True:
            try:
                cb = self.subscriptions[channel].pop()
            except IndexError:
                break
            if isinstance(cb, (weakref.ref,)):
                cb = cb()
            if cb is not None:
                cb(data)

    def run(self):
        for message in self.pubsub.listen():
            if message['type'] != 'message':
                continue
            self.notify(*self.parse_message(message))

