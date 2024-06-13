# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class RobotStatePackageTypeToolCommInfo(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.is_enable = self._io.read_u1()
        self.baudrate = self._io.read_s4be()
        self.parity = self._io.read_s4be()
        self.stopbits = self._io.read_s4be()
        self.tci_modbus_status = self._io.read_u1()
        self.reserved0 = self._io.read_f4be()
        self.reserved1 = self._io.read_f4be()


