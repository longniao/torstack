# -*- coding: utf-8 -*-

'''
torstack.core.websocket.client
websocket client definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

class Client(object):

    def __init__(self, identity, nickname="", email='', avatar='', handler=None):
        self._identity = identity
        self._handler = handler
        self._nickname = nickname
        self._email = email
        self._avatar = avatar

    @property
    def identity(self):
        identity = str(id(self._handler))
        return identity

    @property
    def handler(self):
        return self._handler

    @property
    def nickname(self):
        return self._nickname

    @property
    def email(self):
        return self._email

    @property
    def avatar(self):
        return self._avatar

    def __str__(self):
        return self.identity
