# -*- coding: utf-8 -*-

from torstack.config.parser import Parser

config = Parser()
config.load('/Users/panghe/Per/torstack/examples/__conf/dev.conf')
print(config._dict)

