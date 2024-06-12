# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class RobotStatePackageTypeSafetyState(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.safety_crc_num = self._io.read_s4be()
        self.safety_operational_mode = self._io.read_u1()
        self.is_threeposition_device_enable = self._io.read_u1()
        self.current_elbow_position_x = self._io.read_f8be()
        self.current_elbow_position_y = self._io.read_f8be()
        self.current_elbow_position_z = self._io.read_f8be()
        self.elbow_radius = self._io.read_f8be()


