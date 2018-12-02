# -*- coding: utf-8 -*-

'''
torstack.websocket.message
message model definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''


class Message(object):
    '''
    message for websocket
    '''

    def __init__(self, from_id=None, from_name=None, to_id=None, to_name=None, type=None, content=None, extra=None):
        self.from_id = from_id
        self.from_name = from_name
        self.to_id = to_id
        self.to_name = to_name
        self.type = type
        self.content = content
        self.extra = extra

    def to_json(self):
        return self.__dict__