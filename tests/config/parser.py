# -*- coding: utf-8 -*-

from configparser import ConfigParser
import ast
from torstack.config.parser import Parser

config = Parser()
config.load('/Users/hepang/Git/torstack/examples/__conf/helloworld.conf')
print(config._dict)

