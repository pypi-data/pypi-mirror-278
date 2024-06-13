from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.macho.dyld
import ghidra.program.model.data
import java.lang


class DyldCacheImageInfo(object, ghidra.app.util.bin.format.macho.dyld.DyldCacheImage, ghidra.app.util.bin.StructConverter):
    """
    Represents a dyld_cache_image_info structure.
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
        Create a new {@link DyldCacheImageInfo}.
        @param reader A {@link BinaryReader} positioned at the start of a DYLD image info
        @throws IOException if there was an IO-related problem creating the DYLD image info
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getAddress(self) -> long: ...

    def getClass(self) -> java.lang.Class: ...

    def getPath(self) -> unicode: ...

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
    def address(self) -> long: ...

    @property
    def path(self) -> unicode: ...