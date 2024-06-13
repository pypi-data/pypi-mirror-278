from typing import overload
import ghidra.app.util.bin.format.dwarf
import ghidra.app.util.bin.format.dwarf.attribs
import java.lang


class DWARFAttributeValue(object):
    """
    Base class for all DWARF attribute value implementations.
    """





    def __init__(self, def_: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeDef): ...



    def equals(self, __a0: object) -> bool: ...

    def getAttributeForm(self) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFForm: ...

    def getAttributeName(self) -> unicode: ...

    def getClass(self) -> java.lang.Class: ...

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
    def attributeForm(self) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFForm: ...

    @property
    def attributeName(self) -> unicode: ...