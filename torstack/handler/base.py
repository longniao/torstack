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
from tornado.options import define, options
from torstack.library.string import StringLibrary

MESSAGE_PREFIX = 'msg_'

class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self._session_id = None
        self._session_data = None

    @property
    def session_key(self):
        '''
        session key
        :return:
        '''
        if options.session.get('session_key'):
            return options.session.get('session_key')
        else:
            return 'session_key'

    @property
    def session_id(self):
        '''
        session id
        :return:
        '''
        if not self._session_id:
            session_id = self.get_secure_cookie(self.session_key)
            if session_id:
                self._session_id = session_id if isinstance(session_id, str) else session_id.decode('utf-8')

            # create session id if not exist
            if not self._session_id:
                self._session_id = StringLibrary.gen_uuid()
                print(self.session_key, self._session_id, cookie_config['expires_days'])
                self.set_secure_cookie(self.session_key, self._session_id, expires_days=cookie_config['expires_days'])
        return self._session_id

    @property
    def current_user(self):
        '''
        获取当前用户
        :return:
        '''
        if not self._session_data:
            session_string = self.settings['redis'].get(self.session_id)
            if session_string:
                try:
                    # print('session_string:', session_string)
                    session_string = session_string if isinstance(session_string, str) else session_string.decode(
                        'utf-8')

                    import json
                    self._session_data = json.loads(session_string)
                    # print('user_data:', self.user_data)
                    # 刷新过期时间为30分钟
                    self.settings['redis'].setExpire(self.session_id, 1800)
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    # raise

        return self._session_data


    def set_session_data(self, data):
        '''
        设置session
        :param data:
        :return:
        '''
        if data:
            session_data = dict(
                user_id=data.id,
                user_name=data.user_name,
                nick_name=None,
            )
            session_string = '{"user_id":"%s","user_name":"%s","nick_name":"%s"}' % (session_data['user_id'], session_data['user_name'], session_data['nick_name'])
        else:
            session_data = dict()
            session_string = ''

        # 保存变量
        self._session_data = session_data
        # 保存到redis
        self.settings['redis'].set(self.session_id, session_string)

    def clean_session_data(self):
        '''
        清理session
        :return:
        '''
        self.set_session_data(None)

    def get_json_data(self, data):
        '''
        解析post的json数据
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

    def add_message(self, category, message):
        '''
        增加消息提示
        :param category:
        :param message:
        :return:
        '''
        if category and message:
            itemString = '{"category":"%s","message":"%s"}' % (category, message)
            message_cache_key = MESSAGE_PREFIX + self.session_id
            self.settings['redis'].rpush(message_cache_key, itemString)

    def read_messages(self):
        '''
        读取消息
        :return:
        '''
        message_cache_key = MESSAGE_PREFIX + self.session_id
        lenth = self.settings['redis'].llen(message_cache_key)
        if lenth > 0:
            message = self.settings['redis'].lpop(message_cache_key)
            if message:
                if message is not str:
                    message = message.decode('utf-8')

                message = json.loads(message)
                return message
        return None