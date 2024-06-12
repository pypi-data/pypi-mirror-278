# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Defination(KaitaiStruct):

    class Serial(Enum):
        plc2k6 = 2006

    class Pipeline(Enum):
        plc2k5 = 2005

    class Tunnel(Enum):
        plc2k6 = 2006

    class Http(Enum):
        entrypoint = 80

    class Rpc(Enum):
        plc2k6 = 2006
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        pass


