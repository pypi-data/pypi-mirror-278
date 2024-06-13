from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class UnloadedDriver(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    NAME: unicode = u'_DUMP_UNLOADED_DRIVERS'
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getEndAddress(self) -> long: ...

    def getName(self) -> unicode: ...

    def getNameLength(self) -> int: ...

    def getSize(self) -> long: ...

    def getStartAddress(self) -> long: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setEndAddress(self, __a0: long) -> None: ...

    def setName(self, __a0: unicode) -> None: ...

    def setNameLength(self, __a0: int) -> None: ...

    def setStartAddress(self, __a0: long) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def endAddress(self) -> long: ...

    @endAddress.setter
    def endAddress(self, value: long) -> None: ...

    @property
    def name(self) -> unicode: ...

    @name.setter
    def name(self, value: unicode) -> None: ...

    @property
    def nameLength(self) -> int: ...

    @nameLength.setter
    def nameLength(self, value: int) -> None: ...

    @property
    def size(self) -> long: ...

    @property
    def startAddress(self) -> long: ...

    @startAddress.setter
    def startAddress(self, value: long) -> None: ...