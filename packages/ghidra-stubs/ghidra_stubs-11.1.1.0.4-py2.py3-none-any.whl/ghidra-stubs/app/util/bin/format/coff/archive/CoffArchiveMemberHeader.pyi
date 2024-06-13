from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.coff.archive
import ghidra.program.model.data
import java.lang


class CoffArchiveMemberHeader(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    CAMH_MIN_SIZE: int = 60
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SLASH: unicode = u'/'
    SLASH_SLASH: unicode = u'//'
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType



    def __init__(self, name: unicode, date: long, userId: unicode, groupId: unicode, mode: unicode, size: long, payloadOffset: long, memberOffset: long): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDate(self) -> long:
        """
        Milliseconds since java Date epoch
        @return 
        """
        ...

    def getFileOffset(self) -> long: ...

    def getGroupId(self) -> unicode: ...

    def getGroupIdInt(self) -> int: ...

    def getMode(self) -> unicode: ...

    def getName(self) -> unicode: ...

    def getPayloadOffset(self) -> long: ...

    def getSize(self) -> long: ...

    def getUserId(self) -> unicode: ...

    def getUserIdInt(self) -> int: ...

    def hashCode(self) -> int: ...

    def isCOFF(self) -> bool:
        """
        Returns true if this header contains a COFF file.
        @return true if this header contains a COFF file
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def read(reader: ghidra.app.util.bin.BinaryReader, longNames: ghidra.app.util.bin.format.coff.archive.LongNamesMember) -> ghidra.app.util.bin.format.coff.archive.CoffArchiveMemberHeader:
        """
        Reads a COFF archive member header from the specified {@link BinaryReader reader},
         leaving the file position at the start of the this member's payload.
         <p>
         The archive member's name is fixed up using the specified {@link LongNamesMember longNames}
         object.
         <p>
        @param reader stream from which to read the COFF archive member header from
        @param longNames optional, string table with long file names (only present in some 
         COFF ar formats)
        @return a new {@link CoffArchiveMemberHeader}
        @throws IOException
        """
        ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def COFF(self) -> bool: ...

    @property
    def date(self) -> long: ...

    @property
    def fileOffset(self) -> long: ...

    @property
    def groupId(self) -> unicode: ...

    @property
    def groupIdInt(self) -> int: ...

    @property
    def mode(self) -> unicode: ...

    @property
    def name(self) -> unicode: ...

    @property
    def payloadOffset(self) -> long: ...

    @property
    def size(self) -> long: ...

    @property
    def userId(self) -> unicode: ...

    @property
    def userIdInt(self) -> int: ...