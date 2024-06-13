from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.dwarf
import java.lang


class DWARFAddressListHeader(ghidra.app.util.bin.format.dwarf.DWARFIndirectTableHeader):
    """
    Header at the beginning of a address list table
    """





    def __init__(self, startOffset: long, endOffset: long, firstElementOffset: long, addressSize: int, segmentSelectorSize: int, addrCount: int): ...



    def equals(self, __a0: object) -> bool: ...

    def getAddressSize(self) -> int: ...

    def getClass(self) -> java.lang.Class: ...

    def getEndOffset(self) -> long: ...

    def getFirstElementOffset(self) -> long: ...

    def getOffset(self, index: int, reader: ghidra.app.util.bin.BinaryReader) -> long: ...

    def getSegmentSelectorSize(self) -> int: ...

    def getStartOffset(self) -> long: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def read(reader: ghidra.app.util.bin.BinaryReader, defaultIntSize: int) -> ghidra.app.util.bin.format.dwarf.DWARFAddressListHeader:
        """
        Reads a {@link DWARFAddressListHeader} from the stream.
        @param reader {@link BinaryReader} stream
        @param defaultIntSize native int size for the binary
        @return {@link DWARFAddressListHeader}, or null if end-of-list marker
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
    def addressSize(self) -> int: ...

    @property
    def segmentSelectorSize(self) -> int: ...