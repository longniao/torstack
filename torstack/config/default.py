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
    enable=True,
    prefix='sid_',
    lifetime=1800,  # 60*30
)

# cookie
cookie_config = dict(
    enable=True,
    name='_tsid',
    expires=315360000, # 60*60*24*365*10
    expires_days=3650,
)

# rest
rest_config = dict(
    enable=False,
    allow_remote_access=True,
    token_prefix='token_',
    token_lifetime=315360000,  # 60*60*24*365*10
)

# rest header
rest_header_config = dict(
    token='',
    version='',
    signature='',
    timestamp='',
)

# websocket
websocket_config = dict(
    enable=False,
)

# log
log_config = dict(
    enable=False,
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

# redis
redis_config = dict(
    host='',
    port=6379,
    db=1,
    password=None,
    channel='',
    max_connections=30,
    session_expires_days=30,
    autoconnect=True,
)

# mysql
mysql_config = dict(
    host='',
    port=3306,
    dbname='',
    username='',
    password='',
)

# scheduler config
scheduler_config = dict(
    enable=False,
    autorun=True,
)

# scheduler executors
scheduler_executors = []
