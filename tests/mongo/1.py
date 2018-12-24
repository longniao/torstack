# -*- coding: utf-8 -*-

# 使用Motor
import tornado.gen
import tornado.web
import motor.motor_tornado
import pprint
from tornado.ioloop import IOLoop

client = motor.motor_tornado.MotorClient('mongodb://localhost:27017/')
# client = motor.motor_tornado.MotorClient('localhost', 27017)
db = client.test
# db =client['test_database']
collection = db.test_collection
# collection = db['test_collection']
print(db)
print(collection)
# 使用motor实现mongodb的增删改查

async def do_insert():
    document = {'key': 'value'}
    result = await db.test_collection.insert_one(document)
    print('result %s' % repr(result.inserted_id))

async def do_insert():
    for i in range(10):
        await db.test_collection.insert_one({'id': i, 'name':'name_%s' % i})

async def do_find_one():
    document = await db.test_collection.find_one({'id': 7})
    pprint.pprint(document)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        db = self.settings['db']


application = tornado.web.Application([
    (r'/', MainHandler)
], db=db)

#application.listen(8888)
tornado.ioloop.IOLoop.current().run_sync(do_find_one)