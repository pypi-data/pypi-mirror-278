from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.dwarf
import java.lang


class DWARFLocationList(object):
    """
    A collection of DWARFLocation elements, each which represents a location of an item 
     that is only valid for a certain range of program-counter locations.
    """

    EMPTY: ghidra.app.util.bin.format.dwarf.DWARFLocationList



    def __init__(self, __a0: List[object]): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getFirstLocation(self) -> ghidra.app.util.bin.format.dwarf.DWARFLocation: ...

    def getLocationContaining(self, pc: long) -> ghidra.app.util.bin.format.dwarf.DWARFLocation:
        """
        Get the location that corresponds to the specified PC location.
        @param pc programcounter address
        @return the byte array corresponding to the location expression
        """
        ...

    def hashCode(self) -> int: ...

    def isEmpty(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def readV4(reader: ghidra.app.util.bin.BinaryReader, cu: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit) -> ghidra.app.util.bin.format.dwarf.DWARFLocationList:
        """
        Read a v4 {@link DWARFLocationList} from the debug_loc section.
         <p>
        @param reader stream positioned at the start of a .debug_loc location list
        @param cu the compUnit that refers to the location list
        @return list of DWARF locations (address range and location expression)
        @throws IOException if an I/O error occurs
        """
        ...

    @staticmethod
    def readV5(reader: ghidra.app.util.bin.BinaryReader, cu: ghidra.app.util.bin.format.dwarf.DWARFCompilationUnit) -> ghidra.app.util.bin.format.dwarf.DWARFLocationList:
        """
        Reads a v5 {@link DWARFLocationList} from the debug_loclists stream.
        @param reader stream positioned at the start of a .debug_loclists location list
        @param cu the compUnit that refers to the location list
        @return list of DWARF locations (address range and location expression)
        @throws IOException if an I/O error occurs
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @staticmethod
    def withWildcardRange(expr: List[int]) -> ghidra.app.util.bin.format.dwarf.DWARFLocationList:
        """
        Creates a simple location list containing a single wildcarded range and the specified
         expression bytes.
        @param expr {@link DWARFExpression} bytes
        @return new {@link DWARFLocationList} containing a single wildcarded range
        """
        ...

    @property
    def empty(self) -> bool: ...

    @property
    def firstLocation(self) -> ghidra.app.util.bin.format.dwarf.DWARFLocation: ...