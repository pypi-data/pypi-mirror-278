# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class RobotStatePackageTypeConfigurationData(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.limit_joint_x = []
        for i in range(6):
            self.limit_joint_x.append(RobotStatePackageTypeConfigurationData.LimitJointX(self._io, self, self._root))

        self.max_joint_x = []
        for i in range(6):
            self.max_joint_x.append(RobotStatePackageTypeConfigurationData.MaxJointX(self._io, self, self._root))

        self.default_velocity_joint = self._io.read_f8be()
        self.default_acc_joint = self._io.read_f8be()
        self.default_tool_velocity = self._io.read_f8be()
        self.default_tool_acc = self._io.read_f8be()
        self.eq_radius = self._io.read_f8be()
        self.dh_a_joint_x = []
        for i in range(6):
            self.dh_a_joint_x.append(RobotStatePackageTypeConfigurationData.DhAJointX(self._io, self, self._root))

        self.dh_d_joint_d = []
        for i in range(6):
            self.dh_d_joint_d.append(RobotStatePackageTypeConfigurationData.DhDJointD(self._io, self, self._root))

        self.dh_alpha_joint_x = []
        for i in range(6):
            self.dh_alpha_joint_x.append(RobotStatePackageTypeConfigurationData.DhAlphaJointX(self._io, self, self._root))

        self.dh_theta_joint_x = []
        for i in range(6):
            self.dh_theta_joint_x.append(RobotStatePackageTypeConfigurationData.DhThetaJointX(self._io, self, self._root))

        self.board_version = self._io.read_s4be()
        self.control_box_type = self._io.read_s4be()
        self.robot_type = self._io.read_s4be()
        self.robot_struct = self._io.read_s4be()

    class DhDJointD(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._unnamed0 = self._io.read_f8be()


    class DhAlphaJointX(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._unnamed0 = self._io.read_f8be()


    class DhThetaJointX(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._unnamed0 = self._io.read_f8be()


    class MaxJointX(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.velocity = self._io.read_f8be()
            self.acc = self._io.read_f8be()


    class DhAJointX(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._unnamed0 = self._io.read_f8be()


    class LimitJointX(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.min = self._io.read_f8be()
            self.max = self._io.read_f8be()



