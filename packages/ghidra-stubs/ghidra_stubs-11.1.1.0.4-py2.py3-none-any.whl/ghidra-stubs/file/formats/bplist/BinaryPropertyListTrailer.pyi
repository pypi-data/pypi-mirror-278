from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class BinaryPropertyListTrailer(object, ghidra.app.util.bin.StructConverter):
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



    def __init__(self, __a0: ghidra.app.util.bin.BinaryReader): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getObjectCount(self) -> int: ...

    def getObjectRefSize(self) -> int: ...

    def getOffsetSize(self) -> int: ...

    def getOffsetTable(self) -> List[int]: ...

    def getOffsetTableOffset(self) -> int: ...

    def getTopObject(self) -> int: ...

    def getTrailerIndex(self) -> long: ...

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
    def objectCount(self) -> int: ...

    @property
    def objectRefSize(self) -> int: ...

    @property
    def offsetSize(self) -> int: ...

    @property
    def offsetTable(self) -> List[int]: ...

    @property
    def offsetTableOffset(self) -> int: ...

    @property
    def topObject(self) -> int: ...

    @property
    def trailerIndex(self) -> long: ...