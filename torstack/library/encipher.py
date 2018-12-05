# -*- coding: utf-8 -*-

'''
torstack.library.encipher
encipher library definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import hashlib
from os import urandom
from binascii import b2a_base64
from torstack.library.compat import _xrange

l = [c for c in map(chr, _xrange(256))]
l[47] = '-'
l[43] = '_'
l[61] = '.'
_smap = str('').join(l)
del l

class EncipherLibrary(object):

    @classmethod
    def gen_token(cls, blength=36):
        '''
        :param blength:
        :return:
        '''
        token = (b2a_base64(urandom(blength)))[:-1]
        if isinstance(token, str):
            # PY2
            return token.translate(_smap)[:blength]
        return token.decode('utf-8').translate(_smap)[:blength]

    @classmethod
    def encrypt(cls, password, salt):
        '''
        加密密码
        :return:
        '''
        # 1.创建一个hash对象
        h = hashlib.sha256()
        # 2.填充要加密的数据
        passwordString = password + salt
        h.update(bytes(passwordString, encoding='utf-8'))
        # 3.获取加密结果
        return h.hexdigest()
