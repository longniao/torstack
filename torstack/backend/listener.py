# -*- coding: utf-8 -*-

import json
import threading
from tornado.log import app_log
from interest.core.manager import ClientManager

__author__ = 'longniao@gmail.com'

class Listener(threading.Thread):

    def __init__(self, redis, channels):
        threading.Thread.__init__(self)
        self.redis = redis
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def work(self, item):
        '''
        发送消息
        :param item: redis 消息对象
        :return:
        '''
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        data = item['data']
        if not data or isinstance(data, int):
            return

        app_log.info(data)
        try:
            data = json.loads(data)
            if data.get('to_user') and (data.get('type') != 'groups'):
                ClientManager.send_to(data.get('from_user'), data.get('to_user'), data)
            else:
                ClientManager.send_to_all(data)
        except Exception as ex:
            app_log.exception(ex)

    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == 'KILL':
                self.pubsub.unsubscribe()
                break
            else:
                self.work(item)
