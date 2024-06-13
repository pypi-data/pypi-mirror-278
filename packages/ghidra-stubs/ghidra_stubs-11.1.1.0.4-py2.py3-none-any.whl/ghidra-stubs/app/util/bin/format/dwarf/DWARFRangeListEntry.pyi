from typing import overload
import java.lang


class DWARFRangeListEntry(object):
    """
    DWARF Range List Entry id
    """

    DW_RLE_base_address: int = 5
    DW_RLE_base_addressx: int = 1
    DW_RLE_end_of_list: int = 0
    DW_RLE_offset_pair: int = 4
    DW_RLE_start_end: int = 6
    DW_RLE_start_length: int = 7
    DW_RLE_startx_endx: int = 2
    DW_RLE_startx_length: int = 3



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

