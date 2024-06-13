from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.dwarf
import java.lang


class DWARFLocationListHeader(ghidra.app.util.bin.format.dwarf.DWARFIndirectTableHeader):
    """
    Header found at the start of a set of DWARFLocationList entries, which are stored sequentially
     in the DWARFSectionNames#DEBUG_LOCLISTS section.
    """





    def __init__(self, startOffset: long, endOffset: long, firstElementOffset: long, offsetIntSize: int, offsetEntryCount: int, addressSize: int, segmentSelectorSize: int): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getEndOffset(self) -> long: ...

    def getFirstElementOffset(self) -> long: ...

    def getOffset(self, index: int, reader: ghidra.app.util.bin.BinaryReader) -> long: ...

    def getStartOffset(self) -> long: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def read(reader: ghidra.app.util.bin.BinaryReader, defaultIntSize: int) -> ghidra.app.util.bin.format.dwarf.DWARFLocationListHeader: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

