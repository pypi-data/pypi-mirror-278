from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.file.formats.squashfs
import ghidra.formats.gfilesystem
import ghidra.util.task
import java.io
import java.lang


class SquashUtils(object):




    def __init__(self): ...



    @staticmethod
    def buildDirectoryStructure(__a0: ghidra.file.formats.squashfs.SquashFragmentTable, __a1: ghidra.file.formats.squashfs.SquashDirectoryTable, __a2: ghidra.file.formats.squashfs.SquashInodeTable, __a3: ghidra.formats.gfilesystem.FileSystemIndexHelper, __a4: ghidra.util.task.TaskMonitor) -> None: ...

    @staticmethod
    def byteArrayToReader(__a0: List[int]) -> ghidra.app.util.bin.BinaryReader: ...

    @staticmethod
    def decompressBlock(__a0: ghidra.app.util.bin.BinaryReader, __a1: int, __a2: ghidra.util.task.TaskMonitor) -> List[int]: ...

    @staticmethod
    def decompressBytes(__a0: ghidra.app.util.bin.BinaryReader, __a1: int, __a2: int, __a3: ghidra.util.task.TaskMonitor) -> List[int]: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getDecompressionStream(__a0: java.io.InputStream, __a1: int) -> java.io.InputStream: ...

    @staticmethod
    def getSubInputStream(__a0: ghidra.app.util.bin.BinaryReader, __a1: long) -> java.io.InputStream: ...

    def hashCode(self) -> int: ...

    @staticmethod
    def isSquashFS(__a0: List[int]) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

