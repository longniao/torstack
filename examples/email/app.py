#!/usr/bin/env python
#  -*- coding: utf-8 -*-

'''
torstack.examples.helloworld
a helloworld example written by torstack

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import os
from tornado import gen
from torstack.server import TorStackServer
from torstack.handler.base import BaseHandler

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_PATH = os.path.join(PROJECT_PATH, '__conf')
CONF_FILE = CONF_PATH + os.path.sep + 'email.conf'

from torstack.smtp.manager import SmtpManager

class MainHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        from_mail = 'example@mail.com'
        from_name = 'from_name'
        to_mail = 'example@mail.com'
        to_name = 'to_name'
        subject = ' subject'
        content = '''
            <p>Torstack mail test</p>
            <p><a href="http://github.com/longniao/torstack">Torstack</a></p>
        '''
        SmtpManager.send(from_mail=from_mail, from_name=from_name, to_mail=to_mail, to_name=to_name, subject=subject, content=content, mimetype='html')
        self.write("Mail sended")

def main():
    server = TorStackServer()
    server.config.load(CONF_FILE)
    server.add_handlers([(r"/", MainHandler)])
    server.init_application()
    server.add_smtp()
    server.run()

if __name__ == "__main__":
    main()