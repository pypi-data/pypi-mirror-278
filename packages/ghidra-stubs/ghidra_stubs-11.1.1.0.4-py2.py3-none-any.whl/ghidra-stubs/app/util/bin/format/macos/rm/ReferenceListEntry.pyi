from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class ReferenceListEntry(object, ghidra.app.util.bin.StructConverter):
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







    def equals(self, __a0: object) -> bool: ...

    def getAttributes(self) -> int:
        """
        Returns the resource attributes.
        @return the resource attributes
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getDataOffset(self) -> int:
        """
        Returns the offset from the beginning of the
         resource data to the data for this resource.
        @return the offset to the resource data
        """
        ...

    def getHandle(self) -> int:
        """
        Returns the resource handle.
         This field is reserved.
        @return the resource handle
        """
        ...

    def getID(self) -> int:
        """
        Returns the resource ID.
        @return the resource ID
        """
        ...

    def getName(self) -> unicode: ...

    def getNameOffset(self) -> int:
        """
        Returns the offset from the beginning of the resource
         name list to resource name.
        @return the offset to the resource name
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
    def ID(self) -> int: ...

    @property
    def attributes(self) -> int: ...

    @property
    def dataOffset(self) -> int: ...

    @property
    def handle(self) -> int: ...

    @property
    def name(self) -> unicode: ...

    @property
    def nameOffset(self) -> int: ...