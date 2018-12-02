# -*- coding: utf-8 -*-

'''
torstack.websocket.client
websocket client definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

class Client(object):

    def __init__(self, identity, id='', name='', handler=None):
        self._identity = identity
        self._id = id
        self._name = name
        self._handler = handler

    @property
    def identity(self):
        identity = str(id(self._handler))
        return identity

    @property
    def handler(self):
        return self._handler

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def __str__(self):
        return self.identity
