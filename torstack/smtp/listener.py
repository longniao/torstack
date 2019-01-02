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
import smtplib
from torstack.smtp.manager import SmtpManager
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import COMMASPACE,formatdate
from email import encoders
import time

class SmtpListener(threading.Thread):

    config = None
    client = None

    def __init__(self, config={}):
        threading.Thread.__init__(self)

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
        :param config:
        :return:
        '''
        if not self.client:
            try:
                self.client = smtplib.SMTP(host=self.config.get('host'), port=self.config.get('port'), timeout=self.config.get('timeout'))
                # self.client.set_debuglevel(True)
                # self.client = smtplib.SMTP_SSL()
                self.client.login(self.config.get('username'), self.config.get('password'))
            except Exception as ex:
                self.client = None
                app_log.exception(ex)

    def send(self, email):
        '''
        send email
        :return:
        '''
        if not email or isinstance(email, int):
            return
        try:
            from_email, to_email, subject, content = email['from_mail'], email['to_mail'], email['subject'], email['content']
            message = MIMEText(content)
            message['From'] = from_email
            message['To'] = to_email
            message['Subject'] = subject
            self.client.sendmail(message)
        except Exception as ex:
            SmtpManager.MAIL_LIST.append(email)
            app_log.exception(ex)

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        while True:
            if len(SmtpManager.MAIL_LIST) > 0:
                mail = SmtpManager.MAIL_LIST.pop(0)
                self._create_smtp_client()
                self.send(mail)
