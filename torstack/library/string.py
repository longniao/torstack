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
    def gen_uuid(type=1):
        '''
        uuid
        :return:
        '''
        if type == 1:
            return str(uuid.uuid1())
        elif type == 2:
            return str(uuid.uuid2())
        elif type == 3:
            return str(uuid.uuid3())
        elif type == 4:
            return str(uuid.uuid4())
        elif type == 5:
            return str(uuid.uuid5())

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

    @staticmethod
    def substr(string, start=0, len=10):
        '''
        substr string
        :return:
        '''
        l = list(string)
        return ''.join(l[start:len])
