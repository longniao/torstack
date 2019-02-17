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
import time
import tornado.web
from torstack.exception import BaseException

class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self._session_id = None
        self._session_data = None
        self.config = self.application.config
        self.session = self.application.session
        self.cookie = self.application.cookie
        self.storage = self.application.storage

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
                    raise BaseException('10001', "Unexpected error:", sys.exc_info()[0])

        return self._session_data

    def set_session(self, data):
        '''
        set session
        :param data:
        :return:
        '''
        try:
            if not isinstance(data, dict):
                data = dict(data)
            self.session.set(self.session_id, data)
        except:
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
        if 'redis' not in self.storage:
            return False

        if category and message:
            message = dict(
                category=category,
                message=message,
            )
            message_string = json.dumps(message)
            self.storage['redis'].client.rpush(self.message_id, message_string)

    def read_messages(self, length=1):
        '''
        read flash messages
        :return:
        '''
        if 'redis' not in self.storage:
            return False

        messages = []
        for i in range(length):
            message_string = self.storage['redis'].client.lpop(self.message_id)
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
        try:
            kwargs['current_user'] = self.current_user
            if 'user_messages' not in kwargs:
                kwargs['user_messages'] = self.read_messages()
            return self.render(template, **kwargs)
        except:
            self.gen_http_error(500, "Unexpected error: %s" % sys.exc_info()[0])

    def response_json(self, code=0, data={}, message='success.', **kwargs):
        '''
        rest api result
        :param code:
        :param data:
        :param message:
        :param kwargs:
        :return:
        '''
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        result = dict()
        result['code'] = code
        result['data'] = data
        result['message'] = message
        result['timestamp'] = time.time()
        self.write(json.dumps(result))
        self.finish()

    def gen_http_error(self, status, msg):
        '''
        generate the custom HTTP error
        :param status:
        :param msg:
        :return:
        '''
        self.clear()
        self.set_status(status)
        self.write('<html><body>' + str(msg) + '</body></html>')
        self.finish()

    def get_json_data(self, data):
        '''
        parse request json body
        :return:
        '''
        if data:
            try:
                # data_string = data.decode('utf-8')
                data_json = json.loads(data)
                return data_json
            except Exception as e:
                print('Unable to parse JSON. %s' % e)

        return dict()
