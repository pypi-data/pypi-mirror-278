# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class RobotStatePackageTypeToolData(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.tool_analog_output_domain = self._io.read_u1()
        self.tool_analog_input_domain = self._io.read_u1()
        self.tool_analog_output_value = self._io.read_f8be()
        self.tool_analog_input_value = self._io.read_f8be()
        self.tool_voltage = self._io.read_f4be()
        self.tool_output_voltage = self._io.read_u1()
        self.tool_current = self._io.read_f4be()
        self.tool_temperature = self._io.read_f4be()
        self.tool_mode = self._io.read_u1()


