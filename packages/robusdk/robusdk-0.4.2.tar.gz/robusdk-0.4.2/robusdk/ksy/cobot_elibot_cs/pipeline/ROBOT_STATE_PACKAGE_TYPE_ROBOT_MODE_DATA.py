# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class RobotStatePackageTypeRobotModeData(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.timestamp = self._io.read_u8be()
        self.is_real_robot_connected = self._io.read_u1()
        self.is_real_robot_enabled = self._io.read_u1()
        self.is_robot_power_on = self._io.read_u1()
        self.is_emergency_stopped = self._io.read_u1()
        self.is_robot_protective_stopped = self._io.read_u1()
        self.is_program_running = self._io.read_u1()
        self.is_program_paused = self._io.read_u1()
        self.get_robot_mode = self._io.read_u1()
        self.get_robot_control_mode = self._io.read_u1()
        self.get_target_speed_fraction = self._io.read_f8be()
        self.get_speed_scaling = self._io.read_f8be()
        self.get_target_speed_fraction_limit = self._io.read_f8be()
        self.get_robot_speed_mode = self._io.read_u1()
        self.is_robot_system_in_alarm = self._io.read_u1()
        self.is_in_package_mode = self._io.read_u1()
        self.reverse = self._io.read_u4be()


