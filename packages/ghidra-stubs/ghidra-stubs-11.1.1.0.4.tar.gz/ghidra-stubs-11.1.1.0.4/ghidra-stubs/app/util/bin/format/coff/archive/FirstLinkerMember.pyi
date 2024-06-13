from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class FirstLinkerMember(object, ghidra.app.util.bin.StructConverter):
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



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader, header: ghidra.app.util.bin.format.coff.archive.CoffArchiveMemberHeader, skip: bool): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getFileOffset(self) -> long: ...

    def getNumberOfSymbols(self) -> int: ...

    def getOffsets(self) -> List[int]: ...

    def getStringTable(self) -> List[unicode]: ...

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
    def fileOffset(self) -> long: ...

    @property
    def numberOfSymbols(self) -> int: ...

    @property
    def offsets(self) -> List[int]: ...

    @property
    def stringTable(self) -> List[object]: ...