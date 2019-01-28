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

class SmtpManager(object):

    MAIL_LIST = []

    @classmethod
    def send(cls, from_mail=None, from_name=None, to_mail=None, to_name=None, subject=None, content=None, mimetype='plain', extra=None):
        '''
        send mail
        :param from_mail:
        :param from_name:
        :param to_mail:
        :param to_name:
        :param subject:
        :param content:
        :param mimetype:
        :param extra:
        :return:
        '''
        email = Email(from_mail, from_name, to_mail, to_name, subject, content, mimetype, extra)
        SmtpManager.MAIL_LIST.append(email.to_json())
        return


