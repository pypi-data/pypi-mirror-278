# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Pipeline(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.martching_word = self._io.read_u4be()
        if not self.martching_word == 3967833836:
            raise kaitaistruct.ValidationNotEqualError(3967833836, self.martching_word, self._io, u"/seq/0")
        if self.martching_word == 3967833836:
            self.message_size = self._io.read_u4be()
            if not self.message_size == 1024:
                raise kaitaistruct.ValidationNotEqualError(1024, self.message_size, self._io, u"/seq/1")

        if self.message_size == 1024:
            self.pipeline = self._io.read_bytes(((self.message_size - 4) - 4))

        self.rest = self._io.read_bytes_full()


