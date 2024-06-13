from typing import overload
import ghidra.app.util.bin
import ghidra.file.formats.dump.mdmp
import ghidra.program.model.data
import java.lang


class MemoryInfoListStream(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    NAME: unicode = u'MINIDUMP_MEMORY_INFO_LIST'
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

    def getMemoryInfo(self, __a0: int) -> ghidra.file.formats.dump.mdmp.MemoryInfo: ...

    def getNumberOfEntries(self) -> long: ...

    def getSizeOfEntry(self) -> int: ...

    def getSizeOfHeader(self) -> int: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setMemoryInfo(self, __a0: ghidra.file.formats.dump.mdmp.MemoryInfo, __a1: int) -> None: ...

    def setNumberOfEntries(self, __a0: int) -> None: ...

    def setSizeOfEntry(self, __a0: int) -> None: ...

    def setSizeOfHeader(self, __a0: int) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def numberOfEntries(self) -> long: ...

    @property
    def sizeOfEntry(self) -> int: ...

    @sizeOfEntry.setter
    def sizeOfEntry(self, value: int) -> None: ...

    @property
    def sizeOfHeader(self) -> int: ...

    @sizeOfHeader.setter
    def sizeOfHeader(self, value: int) -> None: ...