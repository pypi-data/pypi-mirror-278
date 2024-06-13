from typing import overload
import ghidra.app.util.bin
import ghidra.file.formats.dump.mdmp
import ghidra.program.model.data
import java.lang


class Memory64ListStream(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    NAME: unicode = u'MINIDUMP_MEMORY_RANGE_64_LIST'
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

    def getBaseRVA(self) -> long: ...

    def getClass(self) -> java.lang.Class: ...

    def getMemoryRange(self, __a0: int) -> ghidra.file.formats.dump.mdmp.MemoryRange64: ...

    def getNumberOfMemoryRanges(self) -> long: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setBaseRVA(self, __a0: long) -> None: ...

    def setMemoryRange(self, __a0: ghidra.file.formats.dump.mdmp.MemoryRange64, __a1: int) -> None: ...

    def setNumberOfMemoryRanges(self, __a0: int) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def baseRVA(self) -> long: ...

    @baseRVA.setter
    def baseRVA(self, value: long) -> None: ...

    @property
    def numberOfMemoryRanges(self) -> long: ...