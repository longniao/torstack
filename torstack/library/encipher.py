# -*- coding: utf-8 -*-

'''
torstack.library.encipher
encipher library definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import hashlib

class EncipherLibrary(object):

    def gen_salt(self, len=8):
        '''
        生成随机种子
        :return:
        '''
        return ''.join(random.sample(string.ascii_letters + string.digits, len))

    def encrypt(self, password, salt):
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
