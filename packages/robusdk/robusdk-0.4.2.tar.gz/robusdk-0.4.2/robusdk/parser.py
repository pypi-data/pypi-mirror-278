#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kaitaistruct import KaitaiStream, BytesIO

def ksy(type):
    async def parse(payload):
        return type(KaitaiStream(BytesIO(payload)))
    return parse
