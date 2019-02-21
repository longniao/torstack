# -*- coding: utf-8 -*-

'''
torstack.websocket.listener
websocket client listener definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import asyncio
import threading
from tornado.log import app_log
import smtplib
from torstack.smtp.manager import SmtpManager
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import COMMASPACE,formatdate
from email import encoders
import time

class SmtpListener(threading.Thread):

    config = None
    client = None

    def __init__(self, config={}):
        threading.Thread.__init__(self)

        if not config:
            raise BaseException('10101', 'error smtp config.')

        self.init_configs(config)
        # self._create_smtp_client()

    def init_configs(self, config={}):
        '''
        Init configurations.
        :param self:
        :param config:
        :return:
        '''
        if not isinstance(config, dict):
            raise BaseException('10101', 'error smtp config.')

        try:
            use_ssl, host, port, username, password = config.get('use_ssl'), config.get('host'), config.get(
                'port'), config.get('username'), config.get('password')

            if not isinstance(host, str):
                raise ValueError('Invalid host')
            if not port:
                raise ValueError('Invalid port')

            self.config = config
        except Exception as e:
            raise Exception('error: %s', str(e))

    def _create_smtp_client(self):
        '''
        create smtp client
        :param config:
        :return:
        '''
        if not self.client:
            try:
                if self.config.get('use_ssl'):
                    self.client = smtplib.SMTP_SSL(timeout=self.config.get('timeout'))
                else:
                    self.client = smtplib.SMTP(timeout=self.config.get('timeout'))
                self.client.connect(host=self.config.get('host'), port=self.config.get('port'))
                self.client.set_debuglevel(0)
                self.client.login(self.config.get('username'), self.config.get('password'))
            except Exception as ex:
                self.client = None
                app_log.exception(ex)

    def send(self, email):
        '''
        send email
        :return:
        '''
        if not email or isinstance(email, int):
            return
        try:
            from_email, from_name, to_email, to_name, subject, content, mimetype = email['from_mail'], email['from_name'], email['to_mail'], email['to_name'], email['subject'], email['content'], email['mimetype']
            message = MIMEText(content, mimetype, 'utf-8')
            message['From'] = formataddr([from_name, from_email])
            message['To'] = formataddr([to_name, to_email])
            message['Subject'] = Header(subject, 'utf-8')
            self.client.sendmail(from_email, [to_email], message.as_string())
        except smtplib.SMTPConnectError as e:
            print('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPAuthenticationError as e:
            print('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPSenderRefused as e:
            print('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPRecipientsRefused as e:
            print('邮件发送失败，收件人被拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPDataError as e:
            print('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPException as e:
            print('邮件发送失败, ', e.message)
        except Exception as ex:
            # SmtpManager.MAIL_LIST.append(email, [to_email], message.as_string())
            app_log.exception(ex)

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        while True:
            if len(SmtpManager.MAIL_LIST) > 0:
                mail = SmtpManager.MAIL_LIST.pop(0)
                self._create_smtp_client()
                self.send(mail)
