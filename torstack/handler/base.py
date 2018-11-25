# -*- coding: utf-8 -*-

'''
torstack.handler.base
basic handler definition.

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

        self.session = self.settings['session']
        self.cookie = self.settings['cookie']

    @property
    def session_id(self):
        '''
        session id
        :return:
        '''
        if not self._session_id:
            session_id = self.get_secure_cookie(self.session.name)
            if session_id:
                self._session_id = session_id if isinstance(session_id, str) else session_id.decode('utf-8')

            # create session id if not exist
            if not self._session_id:
                self._session_id = self.session.id
                self.set_secure_cookie(self.session.name, self._session_id, expires_days=self.session.expires)
        return self._session_id

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

    def save_session(self, data):
        '''
        设置session
        :param data:
        :return:
        '''
        self.session.save(self.session_id, data)

    def clean_session(self):
        '''
        清理session
        :return:
        '''
        self.session.delete(self.session_id)
