# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Rpc(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.m_sync = self._io.read_u1()
        if not self.m_sync == 90:
            raise kaitaistruct.ValidationNotEqualError(90, self.m_sync, self._io, u"/seq/0")
        self.m_version = self._io.read_u1()
        if not self.m_version == 1:
            raise kaitaistruct.ValidationNotEqualError(1, self.m_version, self._io, u"/seq/1")
        self.m_number = self._io.read_u2be()
        self.m_length = self._io.read_u4be()
        self.m_type = self._io.read_u2be()
        self.m_reserved = self._io.read_bytes(6)
        self.m_body = self._io.read_bytes(self.m_length)
        self.rest = self._io.read_bytes_full()


