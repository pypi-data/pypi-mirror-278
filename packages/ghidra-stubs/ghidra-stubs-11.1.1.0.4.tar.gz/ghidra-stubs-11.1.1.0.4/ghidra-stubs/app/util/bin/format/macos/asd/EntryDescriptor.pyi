from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class EntryDescriptor(object, ghidra.app.util.bin.StructConverter):
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



    def __init__(self, entryID: int, offset: int, length: int): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getEntry(self) -> object: ...

    def getEntryID(self) -> int:
        """
        Returns the entry's ID.
         Note: 0 is invalid.
        @return the entry's ID
        """
        ...

    def getLength(self) -> int:
        """
        Returns the length of the entry's data.
         The length can be zero (0).
        @return the length of the entry's data
        """
        ...

    def getOffset(self) -> int:
        """
        The offset from the beginning of the file
         to the beginning of the entry's data.
        @return the offset to entry's data
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
    def entry(self) -> object: ...

    @property
    def entryID(self) -> int: ...

    @property
    def length(self) -> int: ...

    @property
    def offset(self) -> int: ...