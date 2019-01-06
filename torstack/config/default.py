# -*- coding: utf-8 -*-

'''
torstack.config.default
default config definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

# application config ====================================

# base

project_path = ''
port = 8000

# settings
settings = dict(
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
log = dict(
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
session_enable = True
session = dict(
    prefix='sid_',
    lifetime=1800,  # 60*30
    storage='file', # redis|memcache|file, default redis
)
# cookie
cookie_enable = True
cookie = dict(
    name='_tsid',
    expires=315360000, # 60*60*24*365*10
    expires_days=3650,
)

# rest config ====================================

rest_enable = False
rest = dict(
    allow_remote_access=True,
    token_prefix='token_',
    token_lifetime=315360000,  # 60*60*24*365*10
    storage='file',  # redis|memcache|file, default redis
)

# rest header
rest_header = dict(
    Token='',
    Version='',
    Signature='',
    Timestamp='',
)

# rest_response
rest_response = dict(
    code='',
    data={},
    message='',
    timestamp='',
)

# websocket config ====================================

websocket_enable = False
websocket = dict(
    enable=False,
    redis_channel=['channel'],
)

# scheduler config ====================================

scheduler_enable = False
scheduler = dict(
    autorun=True,
    dbname='test',
    storage='sync_mysql',
    tablename='scheduler_job',
)

# scheduler executors
scheduler_executers = []

# storage config ====================================

# mysql
mysql_enable = False
mysql_drive = 'sync' # sync|async|both
mysql = [dict(
    host='127.0.0.1',
    port=3306,
    dbname='',
    username='',
    password='',
    type='master',
)]

# mongodb
mongodb_enable = False
mongodb = [dict(
    host='127.0.0.1',
    port=27017,
    dbname='',
    username='',
    password='',
    type='master',
)]

# postgresql
postgresql_enable = False
postgresql_drive = 'sync' # sync|async|both
postgresql = [dict(
    host='127.0.0.1',
    port=5432,
    dbname='',
    username='',
    password='',
    type='master',
)]

# redis
redis_enable = False
redis = dict(
    host='127.0.0.1',
    port=6379,
    db=1,
    password=None,
    channel='',
    max_connections=30,
    session_expires_days=30,
    autoconnect=True,
)

# memcache
memcache_enable = False
memcache = [dict(
    host='127.0.0.1',
    port=11211,
    weight=1,
)]

# elasticsearch config ====================================

elasticsearch_enable = False
elasticsearch = dict(
    use_ssl=False,
    host='127.0.0.1',
    port=9200,
    http_auth=None,
    request_timeout=None,
    max_clients=10,
)

# smtp config

smtp_enable = False
smtp = dict(
    use_ssl=False,
    host='',
    port=25,
    username='',
    password='',
    timeout=3,
)