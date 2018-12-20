import redis

pool = redis.ConnectionPool(host='127.0.0.1',port=6379, password=None, db=2)
client = redis.StrictRedis(connection_pool=pool, charset="utf-8", decode_responses=True)
client.publish('channel', '{"a":"bbbccccc"}')