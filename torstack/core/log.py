# -*- coding: utf-8 -*-

'''
torstack.core.session
Basic session definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from __future__ import (absolute_import, division, print_function,
                        with_statement)

import json
from datetime import datetime, timedelta
from torstack.library.encipher import EncipherLibrary

class CoreSession(object):

    SESSION_CONFIG = dict(
        enable=True,
        prefix='sid_',
        lifetime=1800, # 60*30
    )

    def __init__(self, driver, config={}):
        self.__init_driver(driver)
        self.__init_config(config)

        self._expires = datetime.utcnow() + timedelta(seconds=self.SESSION_CONFIG.get('lifetime'))


    def __init_config(self, config={}):
        '''
        Init session configurations.
        :param self:
        :param config:
        :return:
        '''
        if config:
            self.SESSION_CONFIG.update(config)


    def __init_driver(self, driver):
        '''
        setup session driver.
        :return:
        '''
        if driver:
            self.driver = driver
        else:
            from torstack.storage.sync_file import SyncFile
            self.driver = SyncFile()


    def _generate_session_id(self, blength=36):
        '''
        generate session id
        :param blength:
        :return:
        '''
        return EncipherLibrary.gen_token(blength)


    def get(self, key, default=None):
        '''
        Return session value with name as key.
        :param key:
        :param default:
        :return:
        '''
        value = self.driver.get(key)
        if value:
            if isinstance(value, str):
                return value
            else:
                return value.decode('utf-8')
        else:
            return default


    def set(self, key, value):
        '''
        Add/Update session value
        :param key:
        :param value:
        :return:
        '''
        if isinstance(value, str):
            session_string = value
        elif isinstance(value, dict):
            session_string = json.dumps(value)
        elif isinstance(value, object):
            session_string = json.dumps(value.__dict__)
        else:
            raise BaseException('10001', 'error data format: %s.' % str(value))

        self.driver.save(key, session_string, self.SESSION_CONFIG['lifetime'])


    def delete(self, key):
        '''
        Delete session key-value pair
        :param key:
        :return:
        '''
        return self.driver.delete(key)


    def keys(self):
        '''
        Return all keys in session object
        :return:
        '''
        return self.driver.keys()


    def flush(self):
        '''
        this method force system to do session data persistence.
        :return:
        '''
        pass

    def set_expires(self, key, lifetime=None):
        '''
        set lifetime
        :param key:
        :param lifetime:
        :return:
        '''
        if not lifetime:
            lifetime = self.expires
        return self.driver.expire(key, lifetime)

    def new_id(self):
        '''
        :return: new session id
        '''
        return self._generate_session_id(36)


    @property
    def expires(self):
        '''
        :return: session expires time
        '''
        return self.SESSION_CONFIG['lifetime']


class SessionMixin(object):

    @property
    def session(self):
        return self._create_mixin(self, '__session_manager', SessionManager)

    def _create_mixin(self, context, inner_property_name, session_handler):
        if not hasattr(context, inner_property_name):
            setattr(context, inner_property_name, session_handler(context))
        return getattr(context, inner_property_name)

