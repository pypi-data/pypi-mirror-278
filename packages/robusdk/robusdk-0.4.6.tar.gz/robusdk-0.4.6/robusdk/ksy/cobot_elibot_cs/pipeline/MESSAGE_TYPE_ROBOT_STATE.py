# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class MessageTypeRobotState(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.robot_state_package_type_robot_mode_data = MessageTypeRobotState.RobotStatePackageTypeRobotModeData(self._io, self, self._root)
        self.robot_state_package_type_joint_data = MessageTypeRobotState.RobotStatePackageTypeJointData(self._io, self, self._root)
        self.robot_state_package_type_cartesian_info = MessageTypeRobotState.RobotStatePackageTypeCartesianInfo(self._io, self, self._root)
        self.robot_state_package_type_configuration_data = MessageTypeRobotState.RobotStatePackageTypeConfigurationData(self._io, self, self._root)
        self.robot_state_package_type_masterboard_data = MessageTypeRobotState.RobotStatePackageTypeMasterboardData(self._io, self, self._root)
        self.robot_state_package_type_additional_info = MessageTypeRobotState.RobotStatePackageTypeAdditionalInfo(self._io, self, self._root)
        self.robot_state_package_type_production_mode = MessageTypeRobotState.RobotStatePackageTypeProductionMode(self._io, self, self._root)
        self.robot_state_package_type_tool_data = MessageTypeRobotState.RobotStatePackageTypeToolData(self._io, self, self._root)
        self.robot_state_package_type_safety_state = MessageTypeRobotState.RobotStatePackageTypeSafetyState(self._io, self, self._root)
        self.robot_state_package_type_tool_comm_info = MessageTypeRobotState.RobotStatePackageTypeToolCommInfo(self._io, self, self._root)
        self.robot_state_package_type_production_mode_data = MessageTypeRobotState.RobotStatePackageTypeProductionModeData(self._io, self, self._root)

    class RobotStatePackageTypeSafetyState(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sub_len = self._io.read_u4be()
            self.sub_type = self._io.read_u1()
            if not self.sub_type == 10:
                raise kaitaistruct.ValidationNotEqualError(10, self.sub_type, self._io, u"/types/robot_state_package_type_safety_state/seq/1")
            self.body = self._io.read_bytes(((self.sub_len - 4) - 1))


    class RobotStatePackageTypeRobotModeData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sub_len = self._io.read_u4be()
            self.sub_type = self._io.read_u1()
            if not self.sub_type == 0:
                raise kaitaistruct.ValidationNotEqualError(0, self.sub_type, self._io, u"/types/robot_state_package_type_robot_mode_data/seq/1")
            self.body = self._io.read_bytes(((self.sub_len - 4) - 1))


    class RobotStatePackageTypeProductionMode(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sub_len = self._io.read_u4be()
            self.sub_type = self._io.read_u1()
            if not self.sub_type == 9:
                raise kaitaistruct.ValidationNotEqualError(9, self.sub_type, self._io, u"/types/robot_state_package_type_production_mode/seq/1")
            self.body = self._io.read_bytes(((self.sub_len - 4) - 1))


    class RobotStatePackageTypeProductionModeData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sub_len = self._io.read_u4be()
            self.sub_type = self._io.read_u1()
            if not self.sub_type == 14:
                raise kaitaistruct.ValidationNotEqualError(14, self.sub_type, self._io, u"/types/robot_state_package_type_production_mode_data/seq/1")
            self.body = self._io.read_bytes(((self.sub_len - 4) - 1))


    class RobotStatePackageTypeToolCommInfo(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sub_len = self._io.read_u4be()
            self.sub_type = self._io.read_u1()
            if not self.sub_type == 11:
                raise kaitaistruct.ValidationNotEqualError(11, self.sub_type, self._io, u"/types/robot_state_package_type_tool_comm_info/seq/1")
            self.body = self._io.read_bytes(((self.sub_len - 4) - 1))


    class RobotStatePackageTypeJointData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sub_len = self._io.read_u4be()
            self.sub_type = self._io.read_u1()
            if not self.sub_type == 1:
                raise kaitaistruct.ValidationNotEqualError(1, self.sub_type, self._io, u"/types/robot_state_package_type_joint_data/seq/1")
            self.body = self._io.read_bytes(((self.sub_len - 4) - 1))


    class RobotStatePackageTypeConfigurationData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sub_len = self._io.read_u4be()
            self.sub_type = self._io.read_u1()
            if not self.sub_type == 6:
                raise kaitaistruct.ValidationNotEqualError(6, self.sub_type, self._io, u"/types/robot_state_package_type_configuration_data/seq/1")
            self.body = self._io.read_bytes(((self.sub_len - 4) - 1))


    class RobotStatePackageTypeToolData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sub_len = self._io.read_u4be()
            self.sub_type = self._io.read_u1()
            if not self.sub_type == 2:
                raise kaitaistruct.ValidationNotEqualError(2, self.sub_type, self._io, u"/types/robot_state_package_type_tool_data/seq/1")
            self.body = self._io.read_bytes(((self.sub_len - 4) - 1))


    class RobotStatePackageTypeCartesianInfo(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sub_len = self._io.read_u4be()
            self.sub_type = self._io.read_u1()
            if not self.sub_type == 4:
                raise kaitaistruct.ValidationNotEqualError(4, self.sub_type, self._io, u"/types/robot_state_package_type_cartesian_info/seq/1")
            self.body = self._io.read_bytes(((self.sub_len - 4) - 1))


    class RobotStatePackageTypeMasterboardData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sub_len = self._io.read_u4be()
            self.sub_type = self._io.read_u1()
            if not self.sub_type == 3:
                raise kaitaistruct.ValidationNotEqualError(3, self.sub_type, self._io, u"/types/robot_state_package_type_masterboard_data/seq/1")
            self.body = self._io.read_bytes(((self.sub_len - 4) - 1))


    class RobotStatePackageTypeAdditionalInfo(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sub_len = self._io.read_u4be()
            self.sub_type = self._io.read_u1()
            if not self.sub_type == 8:
                raise kaitaistruct.ValidationNotEqualError(8, self.sub_type, self._io, u"/types/robot_state_package_type_additional_info/seq/1")
            self.body = self._io.read_bytes(((self.sub_len - 4) - 1))



