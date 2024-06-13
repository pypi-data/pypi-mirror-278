from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.coff.archive
import ghidra.program.model.data
import java.lang


class LongNamesMember(object, ghidra.app.util.bin.StructConverter):
    """
    A string table that contains the full filenames of COFF archive members who's actual
     filenames can not fit in the fixed-length name 
     CoffArchiveMemberHeader#getName().
 
     This string table is held in a special archive member named "//" and is usually one of
     the first members of the archive.
 
     With MS libs, this will typically be the 3rd member in the archive, right after 
     the first and second "/" special members.
    """

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



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader, header: ghidra.app.util.bin.format.coff.archive.CoffArchiveMemberHeader): ...



    def equals(self, __a0: object) -> bool: ...

    def findName(self, provider: ghidra.app.util.bin.ByteProvider, archiveMemberHeader: ghidra.app.util.bin.format.coff.archive.CoffArchiveMemberHeader) -> unicode: ...

    def getClass(self) -> java.lang.Class: ...

    def getFileOffset(self) -> long: ...

    def getStringAtOffset(self, provider: ghidra.app.util.bin.ByteProvider, offset: long) -> unicode: ...

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