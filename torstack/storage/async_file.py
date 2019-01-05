# -*- coding: utf-8 -*-

'''
torstack.storage.redis
redis storage definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import os
import aiofiles

class AsyncFile(object):

    path = '/tmp'

    def __init__(self, path=None):
        if path:
            self.path = path

    def mkdir(self, path):
        '''
        make dir
        :param path:
        :return:
        '''
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)

    def get(self, file):
        '''
        get file content
        :param file:
        :return:
        '''
        path = '%s/%s' % (self.path, file)
        if os.path.exists(path):
            async with aiofiles.open(path, mode='r') as f:
                return await f.read()
        return None

    def save(self, file, content='', lifetime=None):
        '''
        save content to file
        :param file:
        :param content:
        :param lifetime:
        :return:
        '''
        self.mkdir(self.path)
        path = '%s/%s' % (self.path, file)
        async with aiofiles.open(path, mode='w') as f:
            await f.write(content)
        return True

    def delete(self, file):
        '''
        delete file
        :param file:
        :return:
        '''
        path = '%s/%s' % (self.path, file)
        if os.path.exists(path):
            os.remove(path)
        else:
            return True

    def expire(self, key, lifetime=0):
        '''
        do nothing
        '''
        pass

