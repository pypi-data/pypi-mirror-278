from typing import List
from typing import overload
import ghidra.app.util.bin.format.dwarf
import ghidra.app.util.bin.format.dwarf.expression
import java.lang


class DWARFLocation(object):
    """
    Represents the location of an item that is only valid for a certain range of program-counter
     locations.
 
     An instance that does not have a DWARFRange is considered valid for any pc.
    """





    @overload
    def __init__(self, addressRange: ghidra.app.util.bin.format.dwarf.DWARFRange, expr: List[int]): ...

    @overload
    def __init__(self, start: long, end: long, expr: List[int]):
        """
        Create a Location given an address range and location expression.
        @param start start address range
        @param end end of address range
        @param expr bytes of a DWARFExpression
        """
        ...



    def contains(self, addr: long) -> bool: ...

    def equals(self, __a0: object) -> bool: ...

    def evaluate(self, cu: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit) -> ghidra.app.util.bin.format.dwarf.expression.DWARFExpressionResult: ...

    def getClass(self) -> java.lang.Class: ...

    def getExpr(self) -> List[int]: ...

    def getOffset(self, pc: long) -> long: ...

    def getRange(self) -> ghidra.app.util.bin.format.dwarf.DWARFRange: ...

    def hashCode(self) -> int: ...

    def isWildcard(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def expr(self) -> List[int]: ...

    @property
    def range(self) -> ghidra.app.util.bin.format.dwarf.DWARFRange: ...

    @property
    def wildcard(self) -> bool: ...