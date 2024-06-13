from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.dwarf
import java.lang


class DWARFRangeList(object):
    """
    Represents a list of DWARFRanges.
    """

    EMTPY: ghidra.app.util.bin.format.dwarf.DWARFRangeList



    @overload
    def __init__(self, singleRange: ghidra.app.util.bin.format.dwarf.DWARFRange): ...

    @overload
    def __init__(self, __a0: List[object]): ...



    def equals(self, __a0: object) -> bool: ...

    def get(self, index: int) -> ghidra.app.util.bin.format.dwarf.DWARFRange: ...

    def getClass(self) -> java.lang.Class: ...

    def getFirst(self) -> ghidra.app.util.bin.format.dwarf.DWARFRange: ...

    def getFirstAddress(self) -> long: ...

    def getFlattenedRange(self) -> ghidra.app.util.bin.format.dwarf.DWARFRange: ...

    def getLast(self) -> ghidra.app.util.bin.format.dwarf.DWARFRange: ...

    def getListCount(self) -> int: ...

    def hashCode(self) -> int: ...

    def isEmpty(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ranges(self) -> List[ghidra.app.util.bin.format.dwarf.DWARFRange]: ...

    @staticmethod
    def readV4(reader: ghidra.app.util.bin.BinaryReader, cu: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit) -> ghidra.app.util.bin.format.dwarf.DWARFRangeList:
        """
        Reads a v4 {@link DWARFRangeList} from the .debug_ranges stream.
        @param reader stream positioned to the start of a .debug_ranges range list
        @param cu the compUnit referring to this range
        @return new {@link DWARFRangeList}, never null
        @throws IOException if error reading
        """
        ...

    @staticmethod
    def readV5(reader: ghidra.app.util.bin.BinaryReader, cu: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit) -> ghidra.app.util.bin.format.dwarf.DWARFRangeList:
        """
        Reads a v5 {@link DWARFRangeList} from the .debug_rnglists stream.
        @param reader stream positioned to the start of a .debug_rnglists range list
        @param cu the compUnit referring to this range
        @return new {@link DWARFRangeList}, never null
        @throws IOException if error reading
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def empty(self) -> bool: ...

    @property
    def first(self) -> ghidra.app.util.bin.format.dwarf.DWARFRange: ...

    @property
    def firstAddress(self) -> long: ...

    @property
    def flattenedRange(self) -> ghidra.app.util.bin.format.dwarf.DWARFRange: ...

    @property
    def last(self) -> ghidra.app.util.bin.format.dwarf.DWARFRange: ...

    @property
    def listCount(self) -> int: ...