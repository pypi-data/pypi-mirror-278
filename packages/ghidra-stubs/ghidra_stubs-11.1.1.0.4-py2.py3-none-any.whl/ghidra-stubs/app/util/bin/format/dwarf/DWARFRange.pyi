from typing import overload
import ghidra.app.util.bin.format.dwarf
import java.lang


class DWARFRange(object, java.lang.Comparable):
    """
    Holds the start (inclusive) and end (exclusive, 1 past the last included address) addresses 
     of a range.
 
     DWARF ranges are slightly different than Ghidra AddressRange because the
     end address of a Ghidra AddressRange is inclusive, and the DWARF range is exclusive.
 
     DWARF ranges can represent an empty range, Ghidra AddressRanges can not.
     Ghidra AddressRanges can include the maximum 64bit address (0xffffffffffffffff), but DWARF ranges
     can not include that.
    """

    EMPTY: ghidra.app.util.bin.format.dwarf.DWARFRange



    def __init__(self, start: long, end: long):
        """
        Constructs a new {@link DWARFRange} using start and end values.
        @param start long starting address, inclusive
        @param end long ending address, exclusive
        """
        ...



    @overload
    def compareTo(self, other: ghidra.app.util.bin.format.dwarf.DWARFRange) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def contains(self, addr: long) -> bool: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getFrom(self) -> long:
        """
        Returns starting address.
        @return long starting address
        """
        ...

    def getTo(self) -> long:
        """
        Returns ending address, exclusive.
        @return long ending address, exclusive.
        """
        ...

    def hashCode(self) -> int: ...

    def isEmpty(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

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
    def from(self) -> long: ...

    @property
    def to(self) -> long: ...