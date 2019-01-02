# -*- coding: utf-8 -*-

'''
torstack.websocket.manager
websocket client manager definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import json

from tornado.log import app_log

from torstack.smtp.email import Email

MAIL_LIST = []

class SmtpManager(object):

    def send(self, from_mail=None, from_name=None, to_mail=None, to_name=None, content=None, extra=None):
        '''
        send mail
        :param from_mail:
        :param from_name:
        :param to_mail:
        :param to_name:
        :param content:
        :param extra:
        :return:
        '''
        email = Email(from_mail, from_name, to_mail, to_name, content, extra)
        MAIL_LIST.append(email.to_json())
        return client


