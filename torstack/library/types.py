# -*- coding: utf-8 -*-

'''
torstack.library.types
types definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import sys
from datetime import date
boolean = str

if sys.version_info > (3,):
	long = int
	unicode = str
	str = bytes

def convert(value, type):
	""" Convert / Cast function """
	if issubclass(type,str) and not (value.upper() in ['FALSE','TRUE']):
		return value.decode('utf-8')
	elif issubclass(type,unicode):
		return unicode(value)
	elif issubclass(type,int):
		return int(value)
	elif issubclass(type,long):
		return long(value)
	elif issubclass(type,float):
		return float(value)
	elif issubclass(type,boolean) and (value.upper() in ['FALSE','TRUE']):
		if str(value).upper() == 'TRUE': return True
		elif str(value).upper() == 'FALSE': return False
	else:
		return value