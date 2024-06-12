# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class RobotStatePackageTypeJointData(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.joints = []
        for i in range(6):
            self.joints.append(RobotStatePackageTypeJointData.Joints(self._io, self, self._root))


    class Joints(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.actual_joint = self._io.read_f8be()
            self.target_joint = self._io.read_f8be()
            self.actual_velocity = self._io.read_f8be()
            self.target_pluse = self._io.read_s4be()
            self.actual_pluse = self._io.read_s4be()
            self.zero_pluse = self._io.read_s4be()
            self.current = self._io.read_f4be()
            self.voltage = self._io.read_f4be()
            self.temperature = self._io.read_f4be()
            self.torques = self._io.read_f4be()
            self.mode = self._io.read_u1()
            self.reserve = self._io.read_u4be()



