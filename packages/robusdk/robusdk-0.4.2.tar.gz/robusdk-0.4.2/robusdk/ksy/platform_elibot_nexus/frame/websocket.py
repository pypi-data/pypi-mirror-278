# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Websocket(KaitaiStruct):

    class Channel(Enum):
        stream = 0
        datetime = 1
        system = 2
        feed = 3
        cache = 4
        downstream = 16
        pipeline = 17
        hid = 18
        lua = 19
        rpc = 20
        upstream = 32
        serial = 48
        dispatch = 64
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.channel = KaitaiStream.resolve_enum(Websocket.Channel, self._io.read_u1())
        self.payload = self._io.read_bytes_full()


