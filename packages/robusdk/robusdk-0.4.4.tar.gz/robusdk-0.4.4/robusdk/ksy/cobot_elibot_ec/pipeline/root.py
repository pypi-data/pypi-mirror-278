# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Root(KaitaiStruct):

    class AutorunCycelMode(Enum):
        single = 0
        single_cycle = 1
        continuous = 2

    class DragState(Enum):
        off = 0
        on = 1

    class ServoReady(Enum):
        off = 0
        on = 1

    class Collision(Enum):
        off = 0
        on = 1

    class JointAlarmState(Enum):
        off = 0
        on = 1

    class RobotMode(Enum):
        teach = 0
        play = 1
        remotion = 2

    class PowerStatus(Enum):
        power_off = 0
        powering_on = 1
        power_on = 2

    class PrecisePositionStatus(Enum):
        precise = 0
        imprecise = 1

    class CanMotorRun(Enum):
        off = 0
        on = 1

    class HandDragStatus(Enum):
        off = 0
        on = 1

    class BrakeOffStatus(Enum):
        off = 0
        on = 1

    class JbiState(Enum):
        stop = 0
        pause = 1
        emergency_stop = 2
        run = 3
        alarm = 4

    class RobotState(Enum):
        stop = 0
        pause = 1
        emergency_stop = 2
        run = 3
        alarm = 4
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.timestamp = self._io.read_u8be()
        self.autorun_cycel_mode = KaitaiStream.resolve_enum(Root.AutorunCycelMode, self._io.read_u1())
        self.machine_pos = []
        for i in range(8):
            self.machine_pos.append(self._io.read_f8be())

        self.machine_pose = []
        for i in range(6):
            self.machine_pose.append(self._io.read_f8be())

        self.machine_user_pose = []
        for i in range(6):
            self.machine_user_pose.append(self._io.read_f8be())

        self.torque = []
        for i in range(8):
            self.torque.append(self._io.read_f8be())

        self.robot_state = KaitaiStream.resolve_enum(Root.RobotState, self._io.read_s4be())
        self.servo_ready = KaitaiStream.resolve_enum(Root.ServoReady, self._io.read_s4be())
        self.can_motor_run = KaitaiStream.resolve_enum(Root.CanMotorRun, self._io.read_s4be())
        self.motor_speed = []
        for i in range(8):
            self.motor_speed.append(self._io.read_s4be())

        self.robot_mode = KaitaiStream.resolve_enum(Root.RobotMode, self._io.read_s4be())
        self.analog_io_input = []
        for i in range(3):
            self.analog_io_input.append(self._io.read_f8be())

        self.analog_io_output = []
        for i in range(5):
            self.analog_io_output.append(self._io.read_f8be())

        self.digital_io_input = []
        for i in range(64):
            self.digital_io_input.append(self._io.read_bits_int_be(1) != 0)

        self.digital_io_output = []
        for i in range(64):
            self.digital_io_output.append(self._io.read_bits_int_be(1) != 0)

        self._io.align_to_byte()
        self.collision = KaitaiStream.resolve_enum(Root.Collision, self._io.read_u1())
        self.machine_flange_pose = []
        for i in range(6):
            self.machine_flange_pose.append(self._io.read_f8be())

        self.machine_user_flange_pose = []
        for i in range(6):
            self.machine_user_flange_pose.append(self._io.read_f8be())

        self.emergency_stop_state = self._io.read_u1()
        self.tcp_speed = self._io.read_f8be()
        self.joint_speed = []
        for i in range(8):
            self.joint_speed.append(self._io.read_f8be())

        self.tcp_acc = self._io.read_f8be()
        self.joint_acc = []
        for i in range(8):
            self.joint_acc.append(self._io.read_f8be())

        self.joint_temperature = []
        for i in range(6):
            self.joint_temperature.append(self._io.read_f8be())

        self.joint_torque = []
        for i in range(6):
            self.joint_torque.append(self._io.read_f8be())

        self.ext_joint_torques = []
        for i in range(6):
            self.ext_joint_torques.append(self._io.read_f8be())

        self.ext_tcp_torques = []
        for i in range(6):
            self.ext_tcp_torques.append(self._io.read_f8be())

        self.drag_state = KaitaiStream.resolve_enum(Root.DragState, self._io.read_u1())
        self.reserved = KaitaiStream.bytes_strip_right(self._io.read_bytes(106), 0)
        self.force_sensor_data = []
        for i in range(6):
            self.force_sensor_data.append(self._io.read_f8be())

        self.joint_alarm_state = KaitaiStream.resolve_enum(Root.JointAlarmState, self._io.read_u1())
        self.modify_play_speed = self._io.read_u4be()
        self.hand_drag_status = KaitaiStream.resolve_enum(Root.HandDragStatus, self._io.read_u1())
        self.subroutine_increment = self._io.read_u2be()
        self.power_status = KaitaiStream.resolve_enum(Root.PowerStatus, self._io.read_u1())
        self.lua_run_status = self._io.read_u1()
        self.precise_position_status = KaitaiStream.resolve_enum(Root.PrecisePositionStatus, self._io.read_u1())
        self.abs_pulse = []
        for i in range(6):
            self.abs_pulse.append(self._io.read_s4be())

        self.abz_pulse = []
        for i in range(6):
            self.abz_pulse.append(self._io.read_s4be())

        self.cur_line = self._io.read_s4be()
        self.jbi_state = KaitaiStream.resolve_enum(Root.JbiState, self._io.read_u1())
        self.cur_tool_num = self._io.read_bits_int_be(4)
        self.cur_user_num = self._io.read_bits_int_be(4)
        self._io.align_to_byte()
        self.brake_off_status = KaitaiStream.resolve_enum(Root.BrakeOffStatus, self._io.read_u1())


