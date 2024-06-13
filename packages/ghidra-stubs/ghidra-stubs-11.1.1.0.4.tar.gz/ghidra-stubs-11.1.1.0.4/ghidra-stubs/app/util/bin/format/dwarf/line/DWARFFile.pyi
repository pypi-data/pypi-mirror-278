from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.dwarf
import ghidra.app.util.bin.format.dwarf.line
import java.lang


class DWARFFile(object):
    """
    DWARFFile is used to store file or directory entries in the DWARFLine.
    """





    @overload
    def __init__(self, name: unicode): ...

    @overload
    def __init__(self, name: unicode, directory_index: int, modification_time: long, length: long, md5: List[int]):
        """
        Create a new DWARF file entry with the given parameters.
        @param name name of the file
        @param directory_index index of the directory for this file
        @param modification_time modification time of the file
        @param length length of the file
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDirectoryIndex(self) -> int: ...

    def getMD5(self) -> List[int]: ...

    def getModificationTime(self) -> long: ...

    def getName(self) -> unicode: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def readV4(reader: ghidra.app.util.bin.BinaryReader) -> ghidra.app.util.bin.format.dwarf.line.DWARFFile:
        """
        Reads a DWARFFile entry.
        @param reader BinaryReader
        @return new DWARFFile, or null if end-of-list was found
        @throws IOException if error reading
        """
        ...

    @staticmethod
    def readV5(__a0: ghidra.app.util.bin.BinaryReader, __a1: List[object], __a2: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit) -> ghidra.app.util.bin.format.dwarf.line.DWARFFile: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def withName(self, newName: unicode) -> ghidra.app.util.bin.format.dwarf.line.DWARFFile: ...

    @property
    def MD5(self) -> List[int]: ...

    @property
    def directoryIndex(self) -> int: ...

    @property
    def modificationTime(self) -> long: ...

    @property
    def name(self) -> unicode: ...