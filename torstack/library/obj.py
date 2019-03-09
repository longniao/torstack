# -*- coding: utf-8 -*-

'''
torstack.library.obj
object library definition.

:copyright: (c) 2019 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

class ObjLibrary(dict):
    '''
    object 类
    '''
    def to_dict(self, obj):
        '''
        convert object to dict
        :param obj:
        :return:
        '''
        d = {}
        for name in dir(obj):
            value = getattr(obj, name)
            if not name.startswith('__') and not callable(value) and not name.startswith('_'):
                d[name] = value
        return d
