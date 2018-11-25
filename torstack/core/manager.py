# -*- coding: utf-8 -*-

import json
from tornado.log import app_log
from interest.models.client import Client

__author__ = 'longniao@gmail.com'

class CoreClient(object):

    _CLIENTS_MAP = {}

    @classmethod
    def get_clients(cls):
        """
        获取当前连接的clients

        @return:
        """
        return cls._CLIENTS_MAP

    @classmethod
    def get_client_by_user(cls, user_id):
        """
        根据websocket handler id获取当前连接client
        @param identity:
        @return:
        """
        app_log.info("current clients {0}".format(cls.get_clients()))
        try:
            client = cls._CLIENTS_MAP[user_id]
            return client
        except Exception as ex:
            return None

    @classmethod
    def add_client(cls, identity, user_id=None, user_name=None, nick_name=None, handler=None):
        """
        添加新的client
        @param identity: websocket handler 编号
        @param user_id: 用户ID
        @param user_name: 用户名
        @param nick_name: 昵称
        @param handler : websocket handler实例对象
        @return:
        """
        client = Client(identity, user_id=user_id, user_name=user_name, nick_name=nick_name, handler=handler)
        cls._CLIENTS_MAP[user_id] = client
        return client

    @classmethod
    def remove_client(cls, user_id):
        """
        移除client
        @param user_id:
        """
        app_log.debug("remove client[{0}]".format(user_id))
        del cls._CLIENTS_MAP[user_id]

    @classmethod
    def send_to_all(cls, data):

        """
        向所有链接到当前服务器的客户端发送信息
        @param data:
        """
        clients = cls.get_clients()
        for key in clients.keys():
            try:
                print('data:', data)
                clients[key].handler.write_message(json.dumps(data))
            except Exception as ex:
                app_log.exception(ex)

    @classmethod
    def send_to(cls, from_user, to_user, data):

        """
        向特定用户发送消息
        @param source_email: 发送者邮箱
        @param to_email: 接受者邮箱地址
        @param data:
        """
        from_client = cls.get_client_by_email(from_email)
        to_client = cls.get_client_by_email(to_email)
        try:
            # 当自己给自己发送消息时
            if from_email == to_email:
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
    def is_client_connected(cls, user_id):
        """
        检查当前连接的客户端是否已经打开了多个浏览器窗口
        @param email: 用户登录用的电子邮箱地址
        """
        try:
            client = cls.get_client_by_user(user_id)
            if client:
                return True
        except Exception as ex:
            return False



