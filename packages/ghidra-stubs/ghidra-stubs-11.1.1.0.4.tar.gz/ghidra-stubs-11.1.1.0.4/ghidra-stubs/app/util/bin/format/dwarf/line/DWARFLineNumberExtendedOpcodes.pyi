from typing import overload
import java.lang


class DWARFLineNumberExtendedOpcodes(object):
    DW_LNE_define_file: int = 3
    DW_LNE_end_sequence: int = 1
    DW_LNE_hi_user: int = 255
    DW_LNE_lo_user: int = 128
    DW_LNE_set_address: int = 2
    DW_LNE_set_discriminator: int = 4



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
    def toString(value: int) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

