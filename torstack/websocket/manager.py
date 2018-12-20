# -*- coding: utf-8 -*-

'''
torstack.websocket.manager
websocket client manager definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import json

from tornado.log import app_log

from torstack.websocket.client import Client


class ClientManager(object):

    _CLIENTS_MAP = {}

    @classmethod
    def get_clients(cls):
        '''
        get all clients
        :return:
        '''
        return cls._CLIENTS_MAP

    @classmethod
    def get_client_by_id(cls, id):
        '''
        get client by id
        :param id:
        :return:
        '''
        try:
            if id in cls._CLIENTS_MAP:
                return cls._CLIENTS_MAP[id]
            else:
                return None
        except Exception as e:
            return None

    @classmethod
    def add_client(cls, identity, id=None, name=None, handler=None):
        '''
        add new client
        :param identity:
        :param id:
        :param name:
        :param handler:
        :return:
        '''
        client = Client(identity, id=id, name=name, handler=handler)
        cls._CLIENTS_MAP[id] = client
        return client

    @classmethod
    def remove_client(cls, id):
        '''
        remove client
        :param id:
        :return:
        '''
        app_log.debug("remove client[{0}]".format(id))
        del cls._CLIENTS_MAP[id]

    @classmethod
    def send_to_all(cls, data):
        '''
        send message to all clients
        :param data:
        :return:
        '''
        clients = cls.get_clients()
        for key in clients.keys():
            try:
                clients[key].handler.write_message(json.dumps(data))
            except Exception as ex:
                app_log.exception(ex)

    @classmethod
    def send_to(cls, from_id, to_id, data):
        '''
        send message
        :param to:
        :param data:
        :return:
        '''
        from_client = cls.get_client_by_id(from_id)
        to_client = cls.get_client_by_id(to_id)
        app_log.info("ClientManager:send_to:%s -> %s : %s" % (from_id, to_id, data))
        try:
            if from_id == to_id:
                to_client.handler.write_message(json.dumps(data))
            else:
                to_client.handler.write_message(json.dumps(data))
                from_client.handler.write_message(json.dumps(data))
        except Exception as ex:
            app_log.exception()

    @classmethod
    def publish(cls, redis=None, channel=None, message=None):
        redis.publish(channel, message)

    @classmethod
    def is_effective_connect(cls, handlerid):
        for key in cls._CLIENTS_MAP.keys():
            client = cls._CLIENTS_MAP[key]
            if client.identity == handlerid:
                return True
        return False

    @classmethod
    def is_client_connected(cls, id):
        '''
        check client
        :param id:
        :return:
        '''
        try:
            client = cls.get_client_by_id(id)
            if client:
                return True
        except Exception as ex:
            return False



