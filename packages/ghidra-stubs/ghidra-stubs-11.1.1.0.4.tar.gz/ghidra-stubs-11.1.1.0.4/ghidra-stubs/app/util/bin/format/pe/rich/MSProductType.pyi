from typing import List
from typing import overload
import ghidra.app.util.bin.format.pe.rich
import java.lang
import java.util


class MSProductType(java.lang.Enum):
    Assembler: ghidra.app.util.bin.format.pe.rich.MSProductType
    CVTRes: ghidra.app.util.bin.format.pe.rich.MSProductType
    CXX_Compiler: ghidra.app.util.bin.format.pe.rich.MSProductType
    C_Compiler: ghidra.app.util.bin.format.pe.rich.MSProductType
    Export: ghidra.app.util.bin.format.pe.rich.MSProductType
    Import: ghidra.app.util.bin.format.pe.rich.MSProductType
    ImportExport: ghidra.app.util.bin.format.pe.rich.MSProductType
    Linker: ghidra.app.util.bin.format.pe.rich.MSProductType
    Unknown: ghidra.app.util.bin.format.pe.rich.MSProductType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.pe.rich.MSProductType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.pe.rich.MSProductType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

