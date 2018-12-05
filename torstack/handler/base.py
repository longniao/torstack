# -*- coding: utf-8 -*-

'''
torstack.handler.base
web handler definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from __future__ import absolute_import, unicode_literals

import sys
import json
import tornado.web

class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self._session_id = None
        self._session_data = None
        self.db = self.settings['_storage_mysql']
        self.redis = self.settings['_storage_redis']

        self.session = self.settings['session']
        self.cookie = self.settings['cookie']

    @property
    def session_id(self):
        '''
        session id
        :return:
        '''
        if not self._session_id:
            session_id = self.get_secure_cookie(self.cookie.name)
            if session_id:
                self._session_id = session_id if isinstance(session_id, str) else session_id.decode('utf-8')

            # create session id if not exist
            if not self._session_id:
                self._session_id = self.session.new_id()
                self.set_secure_cookie(self.cookie.name, self._session_id, expires_days=self.session.expires)
        return self._session_id

    @property
    def message_id(self):
        '''
        flash message id
        :return:
        '''
        return 'msg_' + self.session_id

    @property
    def current_user(self):
        '''
        current user
        :return:
        '''
        if not self._session_data:
            session_string = self.session.get(self.session_id)
            if session_string:
                try:
                    self._session_data = json.loads(session_string)
                    self.session.set_expires(self.session_id, self.session.expires)
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    # raise

        return self._session_data

    def set_session(self, data):
        '''
        set session
        :param data:
        :return:
        '''
        self.session.set(self.session_id, data)

    def clean_session(self):
        '''
        clean session
        :return:
        '''
        self.session.delete(self.session_id)

    def add_message(self, category, message):
        '''
        add flash message
        :param category:
        :param message:
        :return:
        '''
        if category and message:
            message = dict(
                category=category,
                message=message,
            )
            message_string = json.dumps(message)
            self.redis.client.rpush(self.message_id, message_string)

    def read_messages(self, length=1):
        '''
        read flash messages
        :return:
        '''
        messages = []
        for i in range(length):
            message_string = self.redis.client.lpop(self.message_id)
            if message_string:
                if isinstance(message_string, str):
                    pass
                else:
                    message_string = message_string.decode('utf-8')

                message = json.loads(message_string)
                messages.append(message)

        return messages

    def response(self, template, **kwargs):
        '''
        handler response
        :param template:
        :param args:
        :param kwargs:
        :return:
        '''
        kwargs['current_user'] = self.current_user
        if 'user_messages' not in kwargs:
            kwargs['user_messages'] = self.read_messages()
        print(kwargs)
        return self.render(template, **kwargs)