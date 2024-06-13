from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class SwiftTypeMetadataStructure(object, ghidra.app.util.bin.StructConverter):
    """
    Implemented by all Swift type metadata structures
    """

    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DATA_TYPE_CATEGORY: unicode = u'/SwiftTypeMetadata'
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



    def __init__(self, base: long): ...



    def equals(self, __a0: object) -> bool: ...

    def getBase(self) -> long:
        """
        Gets the base "address" of this {@link SwiftTypeMetadataStructure}
        @return The base "address" of this {@link SwiftTypeMetadataStructure}
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getDescription(self) -> unicode:
        """
        Gets a short description of the {@link SwiftTypeMetadataStructure}
        @return A short description of the {@link SwiftTypeMetadataStructure}
        """
        ...

    def getStructureName(self) -> unicode:
        """
        Gets the name of the {@link SwiftTypeMetadataStructure}
        @return The name of the {@link SwiftTypeMetadataStructure}
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
    def base(self) -> long: ...

    @property
    def description(self) -> unicode: ...

    @property
    def structureName(self) -> unicode: ...