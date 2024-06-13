from typing import List
from typing import overload
import ghidra.app.util.bin.format.dwarf.attribs
import java.lang
import java.util


class DWARFAttributeClass(java.lang.Enum):
    address: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeClass
    addrptr: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeClass
    block: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeClass
    constant: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeClass
    exprloc: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeClass
    flag: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeClass
    lineptr: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeClass
    loclist: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeClass
    loclistsptr: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeClass
    macptr: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeClass
    reference: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeClass
    rnglist: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeClass
    rnglistsptr: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeClass
    string: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeClass
    stroffsetsptr: ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeClass







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeClass: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.dwarf.attribs.DWARFAttributeClass]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

