#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from contextlib import suppress
from asyncio import CancelledError
from broadcaster import Broadcast

class Stream(Broadcast):
    def __init__(self, cobot):
        super().__init__(url='memory://')
        self.cobot = cobot
    async def __aiter__(self):
        with suppress(CancelledError):
            async for frame in self.cobot('message'):
                yield await self.publish(channel=frame.channel, message=frame.payload)
    async def __call__(self, channel):
        async with self.subscribe(channel) as events:
            async for event in events:
                yield event
