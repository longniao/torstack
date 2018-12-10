# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import tornado.web
import tornado.websocket
from tornado import gen
from torstack.handler.base import BaseHandler
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


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        """
        1, 检查当前客户端时候已经打开浏览器窗口，是，发送错误提示信息
        """
        email = self.get_secure_cookie('email')
        nickname = self.get_secure_cookie('nickname')
        if ClientManager.is_client_connected(email):
            app_log.exception("client[{0}] already connected!".format(email))
            self.write_message({

                'type': 'system.error',
                'message': '检测到当前用户已经打开一个窗口，当前窗口自动失效'

            })
        else:
            clients = ClientManager.get_clients()
            # 保存客户端信息
            ClientManager.add_client(str(id(self)), nickname=nickname, email=email, handler=self)
            data = {
                'type': 'add',
                'clients': []
            }
            for key in clients.keys():
                client = clients[key]
                data['clients'].append({
                    "type": "add",
                    "id": client.identity,
                    "nickname": client.nickname,
                    "avatar": client.avatar,
                    "email": client.email
                })
            self.send_to_all(json.dumps(data))

    def on_message(self, message):
        app_log.info(message)

    def on_close(self):
        email = self.get_secure_cookie('email')
        _id = str(id(self))
        if ClientManager.is_effective_connect(_id):
            ClientManager.remove_client(email)
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
        ClientManager.publish(self.settings['redis'], options.redis_channel, data)