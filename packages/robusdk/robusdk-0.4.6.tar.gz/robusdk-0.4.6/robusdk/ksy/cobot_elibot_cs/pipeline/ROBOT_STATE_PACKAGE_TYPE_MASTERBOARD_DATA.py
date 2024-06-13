# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class RobotStatePackageTypeMasterboardData(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.digital_input_bits = self._io.read_s4be()
        self.digital_output_bits = self._io.read_s4be()
        self.standard_analog_input_domain0 = self._io.read_u1()
        self.standard_analog_input_domain1 = self._io.read_u1()
        self.tool_analog_input_domain = self._io.read_u1()
        self.standard_analog_input_value0 = self._io.read_f8be()
        self.standard_analog_input_value1 = self._io.read_f8be()
        self.tool_analog_input_value = self._io.read_f8be()
        self.standard_analog_output_domain0 = self._io.read_u1()
        self.standard_analog_output_domain1 = self._io.read_u1()
        self.tool_analog_output_domain = self._io.read_u1()
        self.standard_analog_output_value0 = self._io.read_f8be()
        self.standard_analog_output_value1 = self._io.read_f8be()
        self.tool_analog_output_value = self._io.read_f8be()
        self.bord_temperature = self._io.read_f4be()
        self.robot_voltage = self._io.read_f4be()
        self.robot_current = self._io.read_f4be()
        self.io_current = self._io.read_f4be()
        self.bord_safe_mode = self._io.read_u1()
        self.is_robot_in_reduced_mode = self._io.read_u1()
        self.get_operational_mode_selector_input = self._io.read_u1()
        self.get_threeposition_enabling_device_input = self._io.read_u1()
        self.masterboard_safety_mode = self._io.read_u1()


