# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json
import tornado.web
import tornado.websocket
from tornado import gen
from torstack.handler.websocket import BaseHandler
from torstack.handler.websocket import WebSocketHandler
from account.user_account_service import UserAccountService
from tornado.log import app_log
from torstack.websocket.manager import ClientManager


class HomeHandler(BaseHandler):
    '''
    home
    '''
    @tornado.web.authenticated
    def get(self):
        params = {
            'username': self.current_user['username'],
            'nickname': self.current_user['nickname'],
            'clients': []
        }
        return self.response('chat/home.html', **params)

    @tornado.web.authenticated
    def post(self):
        to_name = self.get_argument('to_name')
        message = self.get_argument('message')
        data = {
            'from_id': self.current_user['username'],
            'from_name': self.current_user['nickname'],
            'message': message,
            'to_name': to_name,
            'type': 'normal'
        }
        self.redis.publish(self.settings['_config_websocket']['channel'], json.dumps(data))


class WebSocketHandler(WebSocketHandler):

    def open(self):
        """
        1, 检查当前客户端时候已经打开浏览器窗口，是，发送错误提示信息
        """
        username = self.current_user['username']
        nickname = self.current_user['nickname']
        if ClientManager.is_client_connected(username):
            app_log.exception("client[{0}] already connected!".format(username))
            self.write_message({

                'type': 'system.error',
                'message': '检测到当前用户已经打开一个窗口，当前窗口自动失效'

            })
        else:
            clients = ClientManager.get_clients()
            # 保存客户端信息
            client = ClientManager.add_client(str(id(self)), id=username, name=nickname, handler=self)
            data = {
                'type': 'add',
                'clients': []
            }
            for key in clients.keys():
                client = clients[key]
                data['clients'].append({
                    "type": "add",
                    "id": client.identity,
                    "username": client.id,
                    "nickname": client.name,
                })
            self.send_to_all(json.dumps(data))

    def on_message(self, message):
        app_log.info(message)

    def on_close(self):
        print(self.current_user)
        username = self.current_user['username']
        _id = str(id(self))
        if ClientManager.is_effective_connect(_id):
            ClientManager.remove_client(username)
            try:
                data = {
                    "type": "out",
                    "id": _id
                }
                self.send_to_all(json.dumps(data))
            except Exception as ex:
                app_log.exception(ex)
        else:
            app_log.info("非有效连接，关闭页面不影响其他已经打开的页面")

    def send_to_all(self, data):
        ClientManager.publish(self.redis, self.settings['_config_redis']['channel'], data)