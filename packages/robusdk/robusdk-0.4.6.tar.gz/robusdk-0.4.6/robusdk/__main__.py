#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit
from json import dumps
from traceback import format_exc
from asyncio import run
from .stream import Stream
from .logger import Logger

async def __main__(callback):
    async with Stream() as stream:
        return await stream(callback)

def main(callback):
    if __name__ == 'robusdk.__main__':
        try:
            exit(run(__main__(callback)))
        except Exception as error:
            Logger.debug(dumps(format_exc()))
            raise error
