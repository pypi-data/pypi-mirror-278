import snap7
import struct
import ctypes
from snap7.client import error_wrap
from snap7.common import check_error

class MySnap7(snap7.client.Client):
    @error_wrap
    def write_bit(self, area: str, DbNumber, Start, Data):
        Val = struct.pack('B', Data & 0xFF)
        return self._library.Cli_WriteArea(self._pointer, area, DbNumber, Start, 1, snap7.types.S7WLBit, Val)

    def read_bit(self, area: str, DbNumber: int, Port: int):
        type_ = snap7.types.wordlen_to_ctypes[snap7.types.S7WLByte]
        data = (type_ * 1)()
        result = self._library.Cli_ReadArea(self._pointer, area, DbNumber, Port, 1, snap7.types.S7WLBit,
                                            ctypes.byref(data))
        check_error(result, context="client")
        return data