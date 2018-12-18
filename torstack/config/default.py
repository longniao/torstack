# -*- coding: utf-8 -*-

'''
torstack.config.default
default config definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

# application config ====================================

# base

config_project_path = ''
config_port = 8000

# settings
config_settings = dict(
    debug=True,
    cookie_secret="__cookie_secret__",
    xsrf_cookies=True,
    compress_response=True,
    max_threads_num=500,
    login_url="/account",
    template_path="%(project_path)s/website/template",
    static_path="%(project_path)s/website/static",
)

# log
config_log = dict(
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

# base config ====================================

# session
config_session = dict(
    enable=True,
    prefix='sid_',
    lifetime=1800,  # 60*30
    storage='file', # redis|memcache|file, default redis
)
# cookie
config_cookie = dict(
    enable=True,
    name='_tsid',
    expires=315360000, # 60*60*24*365*10
    expires_days=3650,
)

# rest config ====================================

# rest
config_rest = dict(
    enable=False,
    allow_remote_access=True,
    token_prefix='token_',
    token_lifetime=315360000,  # 60*60*24*365*10
)

# rest header
config_rest_header = dict(
    token='',
    version='',
    signature='',
    timestamp='',
)

# websocket config ====================================

# websocket
config_websocket = dict(
    enable=False,
)

# scheduler config ====================================

# scheduler config
config_scheduler = dict(
    enable=False,
    autorun=True,
    dbtype='mysql',
    dbname='test'
)

# scheduler executors
scheduler_executers = []

# storage config ====================================

# mysql
config_mysql_enable = False
config_mysql = [dict(
    host='127.0.0.1',
    port=3306,
    dbname='',
    username='',
    password='',
    type='master',
)]

# mongodb
config_mongodb_enable = False
config_mongodb = dict(
    host='127.0.0.1',
    port=3306,
    dbname='',
    username='',
    password='',
    type='master',
)

# redis
config_redis_enable = False
config_redis = dict(
    host='',
    port=6379,
    db=1,
    password=None,
    channel='',
    max_connections=30,
    session_expires_days=30,
    autoconnect=True,
)

# memcache
config_memcache_enable = False
config_memcache = dict(
    host='',
    port=6379,
    db=1,
    password=None,
)
