# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class RobotStatePackageTypeCartesianInfo(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.tcp_x = self._io.read_f8be()
        self.tcp_y = self._io.read_f8be()
        self.tcp_z = self._io.read_f8be()
        self.rot_x = self._io.read_f8be()
        self.rot_y = self._io.read_f8be()
        self.rot_z = self._io.read_f8be()
        self.offset_px = self._io.read_f8be()
        self.offset_py = self._io.read_f8be()
        self.offset_pz = self._io.read_f8be()
        self.offset_rotx = self._io.read_f8be()
        self.offset_roty = self._io.read_f8be()
        self.offset_rotz = self._io.read_f8be()


