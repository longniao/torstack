# -*- coding: utf-8 -*-

'''
torstack.library.dict
dict library definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

class DictLibrary(dict):
    '''
    可通过 .attr 访问的dict
    '''
    def __getattr__(self, key):
        try:
            if isinstance(self[key], dict):
                return Dict(self[key])
            return self[key]
        except KeyError:
            logger.warning(key+" not in "+str(self))
            return None;

    def __setattr__(self, key, value):
        self[key] = value
