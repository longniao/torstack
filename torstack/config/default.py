# -*- coding: utf-8 -*-

'''
torstack.config.default
default config definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

# application
application_config = dict(
    debug=True,
    port=8888,
    cookie_secret="1qaz2wsx1qaz2wsx1qaz2wsx1qaz2wsx",
    xsrf_cookies=True,
    compress_response=True,
    max_threads_num=500,
    autoreload=True,
    login_url="/login",
    template_path='website/template',
    static_path='website/static',
)

# session
session_config = dict(
    session_key='_tid',
    session_prefix='_',
    session_message='u_msg_',
)

# cookie
cookie_config = dict(
    expires=88473600,
    expires_days=1024,
)

# log
log_config = dict(
    log_level="WARNING",
    log_console=False,
    log_file=True,
    log_path="/tmp/logs/log",
    when="D",
    interval=1,
    backupCount=30,
    fmt="%(asctime)s - %(name)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s",
)

# base
base_config = dict(
    session_storage='redis',
)