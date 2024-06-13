from typing import overload
import java.lang


class DWARFLineNumberStandardOpcodes(object):
    DW_LNS_advance_line: int = 3
    DW_LNS_advance_pc: int = 2
    DW_LNS_const_add_pc: int = 8
    DW_LNS_copy: int = 1
    DW_LNS_fixed_advanced_pc: int = 9
    DW_LNS_negate_statement: int = 6
    DW_LNS_set_basic_block: int = 7
    DW_LNS_set_column: int = 5
    DW_LNS_set_epilog_begin: int = 11
    DW_LNS_set_file: int = 4
    DW_LNS_set_isa: int = 12
    DW_LNS_set_prologue_end: int = 10



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

