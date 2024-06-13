from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.file.formats.ext4
import ghidra.program.model.data
import java.lang


class Ext4IBlock(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType



    @overload
    def __init__(self, __a0: ghidra.app.util.bin.BinaryReader, __a1: bool): ...

    @overload
    def __init__(self, __a0: ghidra.app.util.bin.ByteProvider, __a1: bool): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getExtentEntries(self) -> List[object]: ...

    def getExtra(self) -> List[int]: ...

    def getHeader(self) -> ghidra.file.formats.ext4.Ext4ExtentHeader: ...

    def getIndexEntries(self) -> List[object]: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def readIBlockWithExtents(__a0: ghidra.app.util.bin.ByteProvider, __a1: long) -> ghidra.file.formats.ext4.Ext4IBlock: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def extentEntries(self) -> List[object]: ...

    @property
    def extra(self) -> List[int]: ...

    @property
    def header(self) -> ghidra.file.formats.ext4.Ext4ExtentHeader: ...

    @property
    def indexEntries(self) -> List[object]: ...