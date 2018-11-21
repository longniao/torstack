# -*- coding: utf-8 -*-

'''
torstack.library.string
string library definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import uuid

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