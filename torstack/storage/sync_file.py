# -*- coding: utf-8 -*-

'''
torstack.storage.redis
redis storage definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import os

class SyncFile(object):

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
            with open(path, 'r') as fp:
                return fp.read()
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
        fp = open(path, 'w+')
        fp.write(content)
        fp.close()
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

