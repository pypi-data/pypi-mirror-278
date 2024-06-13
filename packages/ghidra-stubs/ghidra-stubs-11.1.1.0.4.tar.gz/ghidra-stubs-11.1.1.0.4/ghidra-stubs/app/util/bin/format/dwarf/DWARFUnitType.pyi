from typing import overload
import java.lang


class DWARFUnitType(object):
    DW_UT_compile: int = 1
    DW_UT_hi_user: int = 255
    DW_UT_lo_user: int = 128
    DW_UT_partial: int = 3
    DW_UT_skeleton: int = 4
    DW_UT_split_compile: int = 5
    DW_UT_split_type: int = 6
    DW_UT_type: int = 2



    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

