from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class MemoryRange(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    NAME: unicode = u'MINIDUMP_MEMORY_RANGE'
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

    def getDataSize(self) -> int: ...

    def getRVA(self) -> int: ...

    def getStartOfMemoryRange(self) -> long: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setDataSize(self, __a0: int) -> None: ...

    def setRVA(self, __a0: int) -> None: ...

    def setStartOfMemoryRange(self, __a0: long) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def RVA(self) -> int: ...

    @RVA.setter
    def RVA(self, value: int) -> None: ...

    @property
    def dataSize(self) -> int: ...

    @dataSize.setter
    def dataSize(self, value: int) -> None: ...

    @property
    def startOfMemoryRange(self) -> long: ...

    @startOfMemoryRange.setter
    def startOfMemoryRange(self, value: long) -> None: ...