#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from asyncio import TaskGroup

class Coroutine:
    def __init__(self, sequences):
        self.sequences = sequences

    def __await__(self):

        async def __await__():
            async with TaskGroup() as group:
                return [group.create_task(self.task(i)) for i in self.sequences]
        return [i.result() for i in (yield from __await__().__await__())]

    async def task(self, i):
        return await i
