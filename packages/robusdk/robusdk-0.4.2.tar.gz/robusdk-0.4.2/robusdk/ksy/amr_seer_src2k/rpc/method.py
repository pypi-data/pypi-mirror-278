# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Method(KaitaiStruct):

    class RobotOther(Enum):
        softemc_req = 6004

    class RobotConfig(Enum):
        upload_and_loadmap_req = 2025
        lock_req = 4005
        uploadmap_req = 4010
        downloadmap_req = 4011
        removemap_req = 4012

    class RobotTask(Enum):
        translate_req = 3055

    class RobotControl(Enum):
        stop_req = 2000
        reloc_req = 2002
        motion_req = 2010
        loadmap_req = 2022

    class RobotStatus(Enum):
        info_res = 1000
        map_req = 1300
        station_req = 1301
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        pass


