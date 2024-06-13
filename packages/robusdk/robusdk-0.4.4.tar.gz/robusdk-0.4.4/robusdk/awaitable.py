#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from asyncio import sleep, ensure_future

class Awaitable:
    def __init__(self, task, onSuccess=lambda *args: None, onError=lambda *args: None):
        self.task = task
        self.onSuccess = onSuccess
        self.onError = onError
        self.errors = []
    def __await__(self):
        async def __await__():
            async def futures():
                try:
                    async for result in self.task():
                        self.onSuccess(result)
                except Exception as error:
                    self.errors.append(error)
                    self.onError(error)

                if len(self.errors) > 0:
                    raise Exception(self.errors)
                else:
                    return
            return await ensure_future(futures())
        return __await__().__await__()
