import redis
r = redis.Redis()
r.publish('channel', 'send msg')