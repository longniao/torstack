#  -*- coding: utf-8 -*-

import asyncio
import aioredis
from tornado import web, websocket
from tornado.ioloop import IOLoop

connections = []

class WSHandler(websocket.WebSocketHandler):
    def open(self):
        connections.append(self)

    def on_message(self, message):
        print(message)

    def on_close(self):
        connections.remove(self)


class GetHandler(web.RequestHandler):
    def get(self):
        self.render("chat.html")

async def consumer(channel):
    while await channel.wait_message():
        msg = await channel.get(encoding='utf-8')
        for connection in connections:
            await connection.write_message(msg)

async def setup():
    connection = await aioredis.create_redis('redis://localhost')
    channel = await connection.subscribe('channel')
    print('channel:', channel)
    if isinstance(channel, list):
        for c in channel:
            asyncio.ensure_future(consumer(c))
    else:
        asyncio.ensure_future(consumer(channel))


application = web.Application([
    (r'/', GetHandler),
    (r'/chat/', WSHandler),
])


if __name__ == '__main__':
    application.listen(8000)
    loop = IOLoop.current()
    loop.add_callback(setup)
    loop.start()