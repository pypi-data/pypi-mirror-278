from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class LzssCompressionHeader(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    POINTER: ghidra.program.model.data.DataType
    PROBE_BYTES_NEEDED: int = 8
    QWORD: ghidra.program.model.data.DataType
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType



    def __init__(self, __a0: ghidra.app.util.bin.ByteProvider): ...



    def equals(self, __a0: object) -> bool: ...

    def getChecksum(self) -> int: ...

    def getClass(self) -> java.lang.Class: ...

    def getCompressedLength(self) -> int: ...

    def getCompressionType(self) -> int: ...

    def getDecompressedLength(self) -> int: ...

    def getPadding(self) -> List[int]: ...

    def getSignature(self) -> int: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def probe(__a0: List[int]) -> bool: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def checksum(self) -> int: ...

    @property
    def compressedLength(self) -> int: ...

    @property
    def compressionType(self) -> int: ...

    @property
    def decompressedLength(self) -> int: ...

    @property
    def padding(self) -> List[int]: ...

    @property
    def signature(self) -> int: ...