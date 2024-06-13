#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.parse import urlparse, urlunparse
from dataclasses import dataclass
# from cbor2 import loads
from uuid import UUID
from httpx import AsyncClient
from httpx_ws import aconnect_ws
from dacite import from_dict
from .parser import ksy
from .ksy.platform_elibot_nexus.frame.websocket import Websocket as PlatformElibotNexusFrameWebsocket
from .ksy.platform_elibot_nexus.hippo.slave import Slave as PlatformElibotNexusHippoSlave
from .ksy.cobot_elibot_ec.service.pipeline import Pipeline as CobotElibotEcServicePipeline
from .ksy.cobot_elibot_ec.pipeline.root import Root as CobotElibotEcPipelineRoot

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        yield self.match
        raise Exception

    def match(self, *args):
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

@dataclass
class Pipeline:
    uuid: bytes
    name: int
    root: dict

@dataclass
class Frame:
    channel: PlatformElibotNexusFrameWebsocket.Channel
    payload: Pipeline

async def robusdk(url, username, password):
    async with AsyncClient() as client:
        response = await client.request('post', f'''{url}api/token''', json={'username': username, 'password': password})
        response.raise_for_status()
        token = response.json()
        def __init__(application, slave=str(UUID(int=0)), name='default'):
            for case in switch(application):
                if case('rpc') or case('message'):
                    class Client:
                        async def __aiter__(self):
                            url_parts = list(urlparse(url))
                            url_parts[0] = 'ws'
                            url_parts[2] = f'/websocket/{application}/'
                            async with AsyncClient() as client:
                                async with aconnect_ws(urlunparse(url_parts), client, headers={
                                        'authorization': f'Bearer {token}',
                                    }) as websocket:
                                    while True:
                                        message = await websocket.receive_bytes()
                                        frame = await ksy(PlatformElibotNexusFrameWebsocket)(message)
                                        for case in switch(frame.channel):
                                            if case(PlatformElibotNexusFrameWebsocket.Channel.pipeline):
                                                slave = await ksy(PlatformElibotNexusHippoSlave)(frame.payload)
                                                root = await ksy(CobotElibotEcPipelineRoot)(slave.chunk)
                                                yield from_dict(data_class=Frame, data={'channel': frame.channel, 'payload': from_dict(data_class=Pipeline, data={**{'root': vars(root)}, **vars(slave)})})
                                                break
                                            if case():
                                                break
                        def __getattr__(self, prop):
                            class Callable:
                                def __init__(self, *args, **kwargs):
                                    self.current = True
                                    self.args = args
                                    self.kwargs = kwargs

                                def __aiter__(self):
                                    return self

                                async def __anext__(self):
                                    while self.current:
                                        self.current = False
                                        async with AsyncClient() as client:
                                            response = await client.request('post', f'''{url}api/{application}/{name}/{prop}''', params={
                                                'slave': slave
                                            }, json=self.kwargs, headers={
                                                'authorization': f'Bearer {token}',
                                            }, timeout=None)
                                            for case in switch(True):
                                                if case(response.status_code == 200 and response.headers['content-type'] == 'application/json; charset=utf-8'):
                                                    return response.json()
                                                elif case(response.status_code == 200 and response.headers['content-type'] == 'application/octet-stream'):
                                                    return response.text
                                                elif case(response.status_code == 504) or case(response.status_code == 501) or case(response.status_code == 500):
                                                    result = response.json()
                                                    response.reason = result.get('message')
                                                    response.raise_for_status()
                                                else:
                                                    response.raise_for_status()
                                    raise StopAsyncIteration
                            return Callable
                    return Client()

        return __init__
