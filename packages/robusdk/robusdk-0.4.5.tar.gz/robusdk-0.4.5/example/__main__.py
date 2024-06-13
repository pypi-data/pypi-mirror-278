#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import builtins
from traceback import format_exc
from asyncio import run, gather, sleep, wait, FIRST_COMPLETED
from aiostream.stream import preserve
from robusdk import robusdk, Logger, Sequence, Coroutine, Awaitable, Stream
from robusdk.ksy.platform_elibot_nexus.frame.websocket import Websocket as PlatformElibotNexusFrameWebsocket

from example.main import main

async def __main__():
    cobot = await robusdk(
        url='http://172.16.11.70:6680/',
        username='q',
        password='q',
    )
    async with Stream(cobot) as stream:
        builtins.stream = stream
        builtins.cobot = stream.cobot
        builtins.Logger = Logger
        builtins.Sequence = Sequence
        builtins.Coroutine = Coroutine
        builtins.Awaitable = Awaitable
        builtins.sleep = sleep
        builtins.Channel = PlatformElibotNexusFrameWebsocket.Channel
        await wait(map(gather, [preserve(stream), main()]), return_when=FIRST_COMPLETED)

if __name__ == '__main__':
    try:
        run(__main__())
    except Exception:
        Logger.debug(str(format_exc()))
