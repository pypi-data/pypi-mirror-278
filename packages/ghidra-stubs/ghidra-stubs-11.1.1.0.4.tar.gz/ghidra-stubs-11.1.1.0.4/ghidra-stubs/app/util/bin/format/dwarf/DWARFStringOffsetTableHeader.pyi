from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.dwarf
import java.lang


class DWARFStringOffsetTableHeader(ghidra.app.util.bin.format.dwarf.DWARFIndirectTableHeader):
    """
    Table of offsets that point into the string table.  These tables are stored sequentially in the
     DWARFSectionNames#DEBUG_STROFFSETS section.
 
     Elements in the table are referred to by index via DWARFForm#DW_FORM_strx and friends.
 
     The table's #getFirstElementOffset() is referred to by a compUnit's 
     DWARFAttribute#DW_AT_str_offsets_base value.
    """





    def __init__(self, startOffset: long, endOffset: long, firstElementOffset: long, intSize: int, count: int): ...



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
    def readV5(reader: ghidra.app.util.bin.BinaryReader, defaultIntSize: int) -> ghidra.app.util.bin.format.dwarf.DWARFStringOffsetTableHeader:
        """
        Reads a string offset table header (found in the .debug_str_offsets section)
        @param reader {@link BinaryReader}
        @return new {@link DWARFStringOffsetTableHeader} instance
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

