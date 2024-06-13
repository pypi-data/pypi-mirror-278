from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.file.formats.ios.png
import ghidra.program.model.data
import java.lang


class ProcessedPNG(object, ghidra.app.util.bin.StructConverter):
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



    def __init__(self, __a0: ghidra.app.util.bin.BinaryReader, __a1: ghidra.util.task.TaskMonitor): ...



    def equals(self, __a0: object) -> bool: ...

    def getChunkArray(self) -> List[object]: ...

    def getClass(self) -> java.lang.Class: ...

    def getFileSignature(self) -> List[int]: ...

    def getIHDRChunk(self) -> ghidra.file.formats.ios.png.IHDRChunk: ...

    def getTotalLength(self) -> int: ...

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
    def IHDRChunk(self) -> ghidra.file.formats.ios.png.IHDRChunk: ...

    @property
    def chunkArray(self) -> List[object]: ...

    @property
    def fileSignature(self) -> List[int]: ...

    @property
    def totalLength(self) -> int: ...