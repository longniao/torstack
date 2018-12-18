# -*- coding: utf-8 -*-

'''
torstack.storage.redis
redis storage definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import os

class FileStorage(object):

    path = '/tmp'

    def __init__(self, path=None):
        if path:
            FileStorage.path = path

    @classmethod
    def mkdir(cls, path):
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)

    @classmethod
    def get(cls, file):
        path = '%s/%s' % (FileStorage.path, file)
        if os.path.exists(path):
            with open(path, 'r') as fp:
                return fp.read()
        return None

    @classmethod
    def save(cls, file, content='', lifetime=None):
        FileStorage.mkdir(FileStorage.path)
        path = '%s/%s' % (FileStorage.path, file)
        fp = open(path, 'w+')
        fp.write(content)
        fp.close()
        return True

    @classmethod
    def delete(cls, file):
        path = '%s/%s' % (FileStorage.path, file)
        if os.path.exists(path):
            os.remove(path)
        else:
            return True
