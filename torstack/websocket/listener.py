# -*- coding: utf-8 -*-

'''
torstack.websocket.listener
websocket client listener definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import json
import asyncio
import threading
from tornado.log import app_log
from torstack.websocket.manager import ClientManager


class ClientListener(threading.Thread):

    MESSAGE_ACTION = [
        'CLIENT:KILL'
    ]

    def __init__(self, redis, channel):
        threading.Thread.__init__(self)
        self.channel = channel
        self.redis = redis.client
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channel)

    def broadcast(self, message):
        '''
        broadcast message
        :param message:
        :return:
        '''
        if not message or isinstance(message, int):
            return

        try:
            message = json.loads(message)
            if message.get('to_id'):
                ClientManager.send_to(message.get('from_id'), message.get('to_id'), message)
            else:
                ClientManager.send_to_all(message)
        except Exception as ex:
            app_log.exception(ex)

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        for message in self.pubsub.listen():
            if message['type'] != 'message':
                continue
            else:
                channel = message['channel']
                message = message['data']
                if not isinstance(channel, str):
                    channel = channel.decode('utf-8')
                if not isinstance(message, str):
                    message = message.decode('utf-8')

                if channel == self.channel:
                    # force kill client
                    if message == 'CLIENT:KILL':
                        self.pubsub.unsubscribe()
                        break
                    else:
                        self.broadcast(message)
