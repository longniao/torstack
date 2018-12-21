# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json
import tornado.web
import tornado.websocket
from tornado import gen
from torstack.handler.websocket import BaseHandler
from torstack.handler.websocket import WebSocketHandler
from tornado.log import app_log
from torstack.websocket.manager import ClientManager
from account.user_account_service import UserAccountService
from torstack.websocket.message import Message

redis_channel = 'channel'

class HomeHandler(BaseHandler):
    '''
    home
    '''
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        params = {
            'username': self.current_user['username'],
            'nickname': self.current_user['nickname'],
            'clients': []
        }
        return self.response('chat/home.html', **params)

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        message = Message(
            from_id = self.current_user['username'],
            from_name = self.current_user['nickname'],
            type = 'message:text',
            content = self.get_argument('message')
        )
        self.storage['redis'].publish(redis_channel, message.to_string())


class WebSocketHandler(WebSocketHandler):

    def open(self):
        '''
        new client connection
        :return:
        '''
        username = self.current_user['username']
        nickname = self.current_user['nickname']

        if ClientManager.is_client_connected(username):
            app_log.exception("client[{0}] already connected!".format(username))
            self.write_message({
                'type': 'system:error',
                'message': 'another client of this user connected，current connection is invalid'
            })
        else:
            # new client
            ClientManager.add_client(str(id(self)), id=username, name=nickname, handler=self)
            message = Message(
                type='system:in',
                content=u'%s is join' % nickname
            )
            self.send_to_all(message.to_string())

    def on_message(self, message):
        '''
        receive message from client
        :param message:
        :return:
        '''
        app_log.info(message)

    def on_close(self):
        '''
        close websocket connection
        :return:
        '''
        username = self.current_user['username']
        nickname = self.current_user['nickname']

        _id = str(id(self))
        if ClientManager.is_effective_connect(_id):
            ClientManager.remove_client(username)
            try:
                message = Message(
                    type='system:out',
                    content=u'%s is left' % nickname
                )

                self.send_to_all(message.to_string())
            except Exception as ex:
                app_log.exception(ex)
        else:
            app_log.info("error connection")

    def send_to_all(self, message):
        '''
        send message to all
        :param message:
        :return:
        '''
        ClientManager.publish(self.storage['redis'], redis_channel, message)
