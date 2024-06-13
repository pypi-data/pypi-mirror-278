from typing import List
from typing import overload
import ghidra.app.util.bin.format.dwarf
import ghidra.app.util.bin.format.dwarf.attribs
import ghidra.app.util.bin.format.dwarf.expression
import java.lang


class DWARFBlobAttribute(ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeValue):
    """
    DWARF attribute with binary bytes.
    """





    def __init__(self, bytes: List[int], def_: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeDef): ...



    def equals(self, __a0: object) -> bool: ...

    def evaluateExpression(self, cu: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit) -> ghidra.app.util.bin.format.dwarf.expression.DWARFExpressionEvaluator: ...

    def getAttributeForm(self) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFForm: ...

    def getAttributeName(self) -> unicode: ...

    def getBytes(self) -> List[int]: ...

    def getClass(self) -> java.lang.Class: ...

    def getLength(self) -> int: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    def toString(self) -> unicode: ...

    @overload
    def toString(self, compilationUnit: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def bytes(self) -> List[int]: ...

    @property
    def length(self) -> int: ...