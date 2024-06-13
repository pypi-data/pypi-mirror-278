from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class DyldCacheLocalSymbolsEntry(object, ghidra.app.util.bin.StructConverter):
    """
    Represents a dyld_cache_local_symbols_entry structure.
    """

    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader, use64bitOffsets: bool):
        """
        Create a new {@link DyldCacheLocalSymbolsEntry}.
        @param reader A {@link BinaryReader} positioned at the start of a DYLD local symbols entry
        @param use64bitOffsets True if the DYLD local symbol entries use 64-bit dylib offsets; false
           if they use 32-bit
        @throws IOException if there was an IO-related problem creating the DYLD local symbols entry
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDylibOffset(self) -> long:
        """
        {@return The dylib offset}
        """
        ...

    def getNListCount(self) -> int:
        """
        {@return The nlist count}
        """
        ...

    def getNListStartIndex(self) -> int:
        """
        {@return The nlist start index}
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def NListCount(self) -> int: ...

    @property
    def NListStartIndex(self) -> int: ...

    @property
    def dylibOffset(self) -> long: ...