from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.coff.archive
import ghidra.program.model.data
import ghidra.util.task
import java.lang


class CoffArchiveHeader(object, ghidra.app.util.bin.StructConverter):
    """
    A class that represents a COFF archive file (ie. MS .lib files, Unix .ar files)
 
     COFF archives are very primitive compared to containers like ZIP or even TAR.
 
     The name of entries (ie. files) inside the archive is limited to 16 bytes, and to 
     support longer names a couple of different schemes have been invented.  See the
     comments in CoffArchiveMemberHeader#read(BinaryReader, LongNamesMember) for
     decoding the name.
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







    def equals(self, __a0: object) -> bool: ...

    def getArchiveMemberHeaders(self) -> List[ghidra.app.util.bin.format.coff.archive.CoffArchiveMemberHeader]: ...

    def getClass(self) -> java.lang.Class: ...

    def getFirstLinkerMember(self) -> ghidra.app.util.bin.format.coff.archive.FirstLinkerMember: ...

    def getLongNameMember(self) -> ghidra.app.util.bin.format.coff.archive.LongNamesMember: ...

    def getSecondLinkerMember(self) -> ghidra.app.util.bin.format.coff.archive.SecondLinkerMember: ...

    def hashCode(self) -> int: ...

    def isMSFormat(self) -> bool:
        """
        Returns true if this COFF archive seems to be a Microsoft lib file (ie.
         has linker members and other features specific to MS)
        @return 
        """
        ...

    @staticmethod
    def isMatch(provider: ghidra.app.util.bin.ByteProvider) -> bool:
        """
        Returns true if the data contained in the {@link ByteProvider provider} contains
         a COFF Archive file.
         <p>
        @param provider
        @return 
        @throws IOException
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def read(provider: ghidra.app.util.bin.ByteProvider, monitor: ghidra.util.task.TaskMonitor) -> ghidra.app.util.bin.format.coff.archive.CoffArchiveHeader:
        """
        Reads and parses the headers and meta-data in a COFF Archive file.
         <p>
         Returns a {@link CoffArchiveHeader} that has a list of the 
         {@link CoffArchiveMemberHeader members} in the archive.
         <p>
        @param provider
        @param monitor
        @return 
        @throws CoffException
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
    def MSFormat(self) -> bool: ...

    @property
    def archiveMemberHeaders(self) -> List[object]: ...

    @property
    def firstLinkerMember(self) -> ghidra.app.util.bin.format.coff.archive.FirstLinkerMember: ...

    @property
    def longNameMember(self) -> ghidra.app.util.bin.format.coff.archive.LongNamesMember: ...

    @property
    def secondLinkerMember(self) -> ghidra.app.util.bin.format.coff.archive.SecondLinkerMember: ...