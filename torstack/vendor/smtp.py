# -*- coding: utf-8 -*-

'''
torstack.vendor.smtp
smtp definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import threading
import aiosmtplib
from email.mime.text import MIMEText
from tornado.log import app_log


class SmtpService(object):

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
        if not isinstance(configs, dict):
            raise BaseException('10101', 'error mysql config.')

        try:
            use_ssl, host, port, username, password = config.get('use_ssl'), config.get('host'), config.get(
                'port'), config.get('username'), config.get('password')

            if not isinstance(host, str):
                raise ValueError('Invalid host')
            if not port:
                raise ValueError('Invalid port')

            self.smtp = aiosmtplib.SMTP(hostname=host, port=port, loop=loop)
        except Exception as e:
            raise Exception('error: %s', str(e))

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
