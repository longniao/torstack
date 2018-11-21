# -*- coding: utf-8 -*-

'''
torstack.exception
Basic exception definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from __future__ import absolute_import, unicode_literals
import six

from torstack.library.utils import to_binary, to_text


class BaseException(Exception):
    '''
    Base exception for torstack
    '''

    def __init__(self, errcode, errmsg):
        '''
        :param errcode: Error code
        :param errmsg: Error message
        '''
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        _repr = 'Error code: {code}, message: {msg}'.format(
            code=self.errcode,
            msg=self.errmsg
        )
        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)

    def __repr__(self):
        _repr = '{klass}({code}, {msg})'.format(
            klass=self.__class__.__name__,
            code=self.errcode,
            msg=self.errmsg
        )
        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)


class WebException(BaseException):
    '''
    Web exception for torstack
    '''

    def __init__(self, errcode, errmsg, request=None, response=None):
        super(WebException, self).__init__(errcode, errmsg)
        self.request = request
        self.response = response
