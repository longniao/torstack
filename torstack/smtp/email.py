# -*- coding: utf-8 -*-

'''
torstack.smtp.email
email model definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import json

class Email(object):

    def __init__(self, from_mail=None, from_name=None, to_mail=None, to_name=None, subject=None, content=None, mimetype='plain', extra=None):
        self.from_mail = from_mail
        self.from_name = from_name
        self.to_mail = to_mail
        self.to_name = to_name
        self.subject = subject
        self.content = content
        self.mimetype = mimetype
        self.extra = extra

    def to_json(self):
        return self.__dict__

    def to_string(self):
        return json.dumps(self.to_json())