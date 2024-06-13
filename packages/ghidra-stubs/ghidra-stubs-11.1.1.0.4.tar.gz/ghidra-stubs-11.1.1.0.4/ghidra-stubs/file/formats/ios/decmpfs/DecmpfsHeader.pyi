from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class DecmpfsHeader(object, ghidra.app.util.bin.StructConverter):
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



    def __init__(self, __a0: ghidra.app.util.bin.BinaryReader, __a1: int): ...



    def equals(self, __a0: object) -> bool: ...

    def getAttrBytes(self) -> List[int]: ...

    def getClass(self) -> java.lang.Class: ...

    def getCompressionMagic(self) -> unicode: ...

    def getCompressionType(self) -> int: ...

    def getUncompressedSize(self) -> long: ...

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
    def attrBytes(self) -> List[int]: ...

    @property
    def compressionMagic(self) -> unicode: ...

    @property
    def compressionType(self) -> int: ...

    @property
    def uncompressedSize(self) -> long: ...