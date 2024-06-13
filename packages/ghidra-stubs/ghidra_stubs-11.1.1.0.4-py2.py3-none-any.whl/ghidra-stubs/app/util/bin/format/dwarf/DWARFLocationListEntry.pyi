from typing import overload
import java.lang


class DWARFLocationListEntry(object):
    DW_LLE_base_address: int = 6
    DW_LLE_base_addressx: int = 1
    DW_LLE_default_location: int = 5
    DW_LLE_end_of_list: int = 0
    DW_LLE_offset_pair: int = 4
    DW_LLE_start_end: int = 7
    DW_LLE_start_length: int = 8
    DW_LLE_startx_endx: int = 2
    DW_LLE_startx_length: int = 3



    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def toString(value: long) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

