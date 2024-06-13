from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.macos.asd
import ghidra.program.model.data
import java.lang


class AppleSingleDouble(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DOUBLE_MAGIC_NUMBER: int = 333319
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SINGLE_MAGIC_NUMBER: int = 333312
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType



    def __init__(self, provider: ghidra.app.util.bin.ByteProvider): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getEntryList(self) -> List[ghidra.app.util.bin.format.macos.asd.EntryDescriptor]: ...

    def getFiller(self) -> List[int]: ...

    def getMagicNumber(self) -> int: ...

    def getNumberOfEntries(self) -> int: ...

    def getVersionNumber(self) -> int: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def entryList(self) -> List[object]: ...

    @property
    def filler(self) -> List[int]: ...

    @property
    def magicNumber(self) -> int: ...

    @property
    def numberOfEntries(self) -> int: ...

    @property
    def versionNumber(self) -> int: ...