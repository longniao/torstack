# -*- coding: utf-8 -*-

'''
torstack.tool.model
model tool definition.

:copyright: (c) 2019 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

# sqlacodegen 'mysql://work:work@127.0.0.1:3306/spider --outfile ./models.py'

import os

class ModelCreater(object):

    def __init__(self):
        pass

    def load_config(self, config={}):
        '''
        加载配置
        :param configs:
        :return:
        '''
        if config.has_key('mysqlDatabase'):
            self.mysqlDatabase = config['mysqlDatabase']
        if config.has_key('modelPath'):
            self.modelPath = config['modelPath']
        if config.has_key('host'):
            self.host = config['host']
        if config.has_key('port'):
            self.port = config['port']
        if config.has_key('username'):
            self.username = config['username']
        if config.has_key('password'):
            self.password = config['password']


    def run(self):
        '''
        执行生成代码
        :return:
        '''
        if not self.mysqlDatabase or not isinstance(self.mysqlDatabase, list):
            raise ValueError("Error config")

        # 分析api
        for db in self.mysqlDatabase:
            outfile = self.modelPath+db+".py"
            code = "sqlacodegen mysql://"+self.username+":"+self.password+"@"+self.host+":"+self.port+"/"+db+" --outfile "+outfile
            os.system(code)
            print db, '-->', outfile

        print 'generate model success...'