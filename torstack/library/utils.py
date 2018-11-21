# -*- coding: utf-8 -*-

'''
torstack.library.utils
utils library definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

def to_text(value, encoding='utf-8'):
    '''
    Convert value to unicode, default encoding is utf-8
    :param value: Value to be converted
    :param encoding: Desired encoding
    :return:
    '''
    if not value:
        return ''
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)


def to_binary(value, encoding='utf-8'):
    '''
    Convert value to binary string, default encoding is utf-8
    :param value: Value to be converted
    :param encoding: Desired encoding
    :return:
    '''
    if not value:
        return b''
    if isinstance(value, six.binary_type):
        return value
    if isinstance(value, six.text_type):
        return value.encode(encoding)
    return six.binary_type(value)