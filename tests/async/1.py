#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio

from aiohttp import web


async def index(request):
    body = b'Hello world'
    return web.Response(body='<h1>是打发斯蒂芬, %s!</h1>'.encode('utf-8'))


async def hello(request):
    await asyncio.sleep(0.5)
    h = request.GET["sdf"]
    text = '<h1>是打发斯蒂芬, %s!</h1>' % request.match_info['name']
    return web.Response(text=text)


async def df(request):
    await asyncio.sleep(0.5)
    # ll = await request.post.get["asdfad"]
    sdf = await request.post()
    sf = sdf.get("asdfad")
    text = '<h1>hello, %s!</h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'))


async def jsonpost(request):
    await asyncio.sleep(0.5)
    # ll = await request.post.get["asdfad"]
    sdf = await request.json()
    sdf = sdf["data"]

    return web.json_response({"fadfadf": 1})


app = web.Application()
app.router.add_route('GET', '/', index)
app.router.add_route('GET', '/{name}', hello)
app.router.add_route("POST", "/hello", jsonpost)
# app.router.add_route("POST", "/hello", df)
web.run_app(app, port=8888, shutdown_timeout=15)