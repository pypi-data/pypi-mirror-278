from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.dwarf
import ghidra.util.task
import java.lang


class DWARFUnitHeader(object):
    """
    The base class for a set of headers that share a common field layout.
    """









    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDWARFVersion(self) -> int: ...

    def getEndOffset(self) -> long:
        """
        Returns the byte offset to the end of this unit.
        @return the byte offset to the end of this unit
        """
        ...

    def getIntSize(self) -> int:
        """
        Returns either 4 (for DWARF_32) or 8 (for DWARF_64) depending on the current unit format
        @return size of ints in this unit (4 or 8)
        """
        ...

    def getProgram(self) -> ghidra.app.util.bin.format.dwarf.DWARFProgram: ...

    def getStartOffset(self) -> long:
        """
        Returns the byte offset to the start of this unit.
        @return the byte offset to the start of this unit
        """
        ...

    def getUnitNumber(self) -> int:
        """
        Return the ordinal number of this unit
        @return ordinal of this unit
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def read(dprog: ghidra.app.util.bin.format.dwarf.DWARFProgram, reader: ghidra.app.util.bin.BinaryReader, abbrReader: ghidra.app.util.bin.BinaryReader, unitNumber: int, monitor: ghidra.util.task.TaskMonitor) -> ghidra.app.util.bin.format.dwarf.DWARFUnitHeader:
        """
        Reads the initial fields found in a unit header.
        @param dprog {@link DWARFProgram}
        @param reader {@link BinaryReader} stream
        @param abbrReader {@link BinaryReader} .debug_abbr stream
        @param unitNumber ordinal of this item
        @param monitor {@link TaskMonitor}
        @return a unit header (only comp units for now), or null if at end-of-list
        @throws DWARFException if invalid dwarf data
        @throws IOException if error reading data
        @throws CancelledException if cancelled
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
    def DWARFVersion(self) -> int: ...

    @property
    def endOffset(self) -> long: ...

    @property
    def intSize(self) -> int: ...

    @property
    def program(self) -> ghidra.app.util.bin.format.dwarf.DWARFProgram: ...

    @property
    def startOffset(self) -> long: ...

    @property
    def unitNumber(self) -> int: ...