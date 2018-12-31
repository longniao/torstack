# -*- coding: utf-8 -*-

'''
torstack.websocket.listener
websocket client listener definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import asyncio
import threading
from tornado.log import app_log
from torstack.websocket.manager import ClientManager
import aiosmtplib
from email.mime.text import MIMEText

MAIL_LIST = []

class SmtpListener(threading.Thread):

    config = None
    smtp = None

    def __init__(self, config={}):
        if not config:
            raise BaseException('10101', 'error smtp config.')

        self.init_configs(config)

    def init_configs(self, config={}):
        '''
        Init configurations.
        :param self:
        :param config:
        :return:
        '''
        if not isinstance(config, dict):
            raise BaseException('10101', 'error mysql config.')

        try:
            use_ssl, host, port, username, password = config.get('use_ssl'), config.get('host'), config.get(
                'port'), config.get('username'), config.get('password')

            if not isinstance(host, str):
                raise ValueError('Invalid host')
            if not port:
                raise ValueError('Invalid port')

            self.config = config
        except Exception as e:
            raise Exception('error: %s', str(e))

    def _create_smtp_client(self):
        '''
        create smtp client
        :return:
        '''
        if self.smtp == None:
            self.smtp = aiosmtplib.SMTP(hostname=host, port=port, loop=loop)

    def send_email(self, from_email, to_email, subject, content):
        '''
        send email
        :param to:
        :param subject:
        :param content:
        :return:
        '''
        message = MIMEText(content)
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = subject
        return self.smtp.send_message(message)

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
        self._create_smtp_client()

        if len(MAIL_LIST) > 0:
            mail = MAIL_LIST[0]
            self.send_email(mail)
            MAIL_LIST.pop(0)
