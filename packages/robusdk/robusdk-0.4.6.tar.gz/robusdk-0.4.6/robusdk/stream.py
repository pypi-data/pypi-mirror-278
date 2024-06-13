#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import builtins
from contextlib import suppress
from asyncio import CancelledError, gather, wait, FIRST_COMPLETED, sleep
from broadcaster import Broadcast
from aiostream.stream import preserve
from .ksy.platform_elibot_nexus.frame.websocket import Websocket as PlatformElibotNexusFrameWebsocket
from .main import robusdk
from .logger import Logger
from .coroutine import Coroutine
from .sequence import Sequence
from .awaitable import Awaitable

class Observable(Broadcast):
    def __init__(self, cobot):
        super().__init__(url='memory://')
        self.cobot = cobot
    async def __aiter__(self):
        yield
        with suppress(CancelledError):
            async for frame in self.cobot('message'):
                yield await self.publish(channel=frame.channel, message=frame.payload)
    async def __call__(self, channel):
        async with self.subscribe(channel) as events:
            async for event in events:
                yield event

class Stream:
    def __init__(self):
        self.cobot = None
        self.stream = None
    def __await__(self):
        return self.closure().__await__()
    async def closure(self):
        self.cobot = await robusdk(
            url='http://172.16.11.70:6680/',
            username='q',
            password='q',
        )
        self.stream = Observable(self.cobot)
        return self
    async def __aenter__(self):
        await self
        await self.stream.__aenter__()
        return self
    async def __aexit__(self, *args, **kwargs):
        return await self.stream.__aexit__(*args, **kwargs)
    async def __call__(self, main):
        builtins.stream = self.stream
        builtins.cobot = self.stream.cobot
        builtins.Logger = Logger
        builtins.Sequence = Sequence
        builtins.Coroutine = Coroutine
        builtins.Awaitable = Awaitable
        builtins.sleep = sleep
        builtins.Channel = PlatformElibotNexusFrameWebsocket.Channel
        return next(iter(next(iter(next(iter(await wait(map(gather, [preserve(self.stream), main()]), return_when=FIRST_COMPLETED))))).result()))
