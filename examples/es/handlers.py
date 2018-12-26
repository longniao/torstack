# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from tornado import gen
from torstack.handler.base import BaseHandler

class ElasticsearchHandler(BaseHandler):
    '''
    AccountHandler
    '''
    def initialize(self):
        super(ElasticsearchHandler, self).initialize()
        self.es = self.application.elasticsearch

class MainHandler(ElasticsearchHandler):

    @gen.coroutine
    def get(self, *args, **kwargs):
        if self.get_argument('id', None):
            result = yield self.es.get(index='test', doc_type='tweet',
                                       id=self.get_argument('id'))
        else:
            result = yield self.es.search(index='test')
        self.finish(result)

    @gen.coroutine
    def post(self, *args, **kwargs):
        doc = {
            'author': self.get_current_user() or 'Unknown',
            'text': self.get_argument('text'),
            'timestamp': datetime.datetime.now()
        }
        result = yield self.es.index(index='test',
                                     doc_type='tweet',
                                     body=doc,
                                     id=str(uuid.uuid4()))
        self.finish(result)

    @gen.coroutine
    def delete(self, *args, **kwargs):
        result = yield self.es.delete(index='test', doc_type='tweet',
                                      id=self.get_argument('id'))
        self.finish(result)