# -*- coding: utf-8 -*-

'''
torstack.library.string
string library definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import uuid
import random
import string

class StringLibrary(object):
    '''
    string library
    '''

    @staticmethod
    def gen_uuid():
        '''
        uuid
        :return:
        '''
        return str(uuid.uuid4())

    @staticmethod
    def gen_random_letters(len=8):
        '''
        gen random letters
        :return:
        '''
        return ''.join(random.sample(string.ascii_letters, len))

    @staticmethod
    def gen_random_numbers(len=8):
        '''
        gen random numbers
        :return:
        '''
        return ''.join(random.sample(string.digits, len))

    @staticmethod
    def gen_random(len=8):
        '''
        gen random letters and numbers
        :return:
        '''
        return ''.join(random.sample(string.ascii_letters + string.digits, len))
