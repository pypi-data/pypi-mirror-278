from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class DyldSubcacheEntry(object, ghidra.app.util.bin.StructConverter):
    """
    Represents a dyld_subcache_entry structure.
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



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader):
        """
        Create a new {@link DyldSubcacheEntry}.
        @param reader A {@link BinaryReader} positioned at the start of a DYLD subCache entry
        @throws IOException if there was an IO-related problem creating the DYLD subCache entry
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getCacheExtension(self) -> unicode:
        """
        Gets the extension of this subCache, if it is known
        @return The extension of this subCache, or null if it is not known
        """
        ...

    def getCacheVMOffset(self) -> long:
        """
        Gets the offset of this subCache from the main cache base address
        @return The offset of this subCache from the main cache base address
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getUuid(self) -> unicode:
        """
        Gets the UUID of the subCache file
        @return The UUID of the subCache file
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
    def cacheExtension(self) -> unicode: ...

    @property
    def cacheVMOffset(self) -> long: ...

    @property
    def uuid(self) -> unicode: ...