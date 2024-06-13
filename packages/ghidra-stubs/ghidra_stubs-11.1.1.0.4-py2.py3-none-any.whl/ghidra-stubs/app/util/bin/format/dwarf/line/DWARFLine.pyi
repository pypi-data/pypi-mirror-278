from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.dwarf
import ghidra.app.util.bin.format.dwarf.line
import ghidra.app.util.bin.format.dwarf.line.DWARFLine
import java.lang


class DWARFLine(object):
    """
    A structure read from .debug_line, contains indexed source filenames as well as a mapping between
     addresses and source filename and linenumbers.
 
     TODO: refactor this and other similar classes to derive from DWARFUnitHeader and simplify
    """






    class SourceFileAddr(java.lang.Record):




        def __init__(self, __a0: long, __a1: unicode, __a2: int): ...



        def address(self) -> long: ...

        def equals(self, __a0: object) -> bool: ...

        def fileName(self) -> unicode: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def lineNum(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...







    @staticmethod
    def empty() -> ghidra.app.util.bin.format.dwarf.line.DWARFLine:
        """
        Returns a dummy DWARFLine instance that contains no information.
        @return {@link DWARFLine} instance with no info
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getAllSourceFileAddrInfo(self, cu: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit, reader: ghidra.app.util.bin.BinaryReader) -> List[ghidra.app.util.bin.format.dwarf.line.DWARFLine.SourceFileAddr]: ...

    def getClass(self) -> java.lang.Class: ...

    def getDir(self, index: int) -> ghidra.app.util.bin.format.dwarf.line.DWARFFile: ...

    def getEndOffset(self) -> long: ...

    def getFile(self, index: int) -> ghidra.app.util.bin.format.dwarf.line.DWARFFile:
        """
        Get a file name given a file index.
        @param index index of the file
        @return file {@link DWARFFile}
        @throws IOException if invalid index
        """
        ...

    def getFilePath(self, index: int, includePath: bool) -> unicode: ...

    def getLineProgramexecutor(self, cu: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit, reader: ghidra.app.util.bin.BinaryReader) -> ghidra.app.util.bin.format.dwarf.line.DWARFLineProgramExecutor: ...

    def getStartOffset(self) -> long: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def read(reader: ghidra.app.util.bin.BinaryReader, defaultIntSize: int, cu: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit) -> ghidra.app.util.bin.format.dwarf.line.DWARFLine: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def endOffset(self) -> long: ...

    @property
    def startOffset(self) -> long: ...