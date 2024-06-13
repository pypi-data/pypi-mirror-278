from typing import List
from typing import overload
import ghidra.app.util.bin.format.dwarf
import java.lang
import java.util


class DWARFIdentifierCase(java.lang.Enum):
    DW_ID_case_insensitive: ghidra.app.util.bin.format.dwarf.DWARFIdentifierCase
    DW_ID_case_sensitive: ghidra.app.util.bin.format.dwarf.DWARFIdentifierCase
    DW_ID_down_case: ghidra.app.util.bin.format.dwarf.DWARFIdentifierCase
    DW_ID_up_case: ghidra.app.util.bin.format.dwarf.DWARFIdentifierCase







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def find(__a0: long) -> ghidra.app.util.bin.format.dwarf.DWARFIdentifierCase: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def getValue(self) -> int: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.dwarf.DWARFIdentifierCase: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.dwarf.DWARFIdentifierCase]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def value(self) -> int: ...