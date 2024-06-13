from typing import List
from typing import overload
import ghidra.app.util.bin.format.swift
import ghidra.program.model.data
import java.lang


class MultiPayloadEnumDescriptor(ghidra.app.util.bin.format.swift.SwiftTypeMetadataStructure):
    """
    Represents a Swift MultiPayloadEnumDescriptor structure
    """

    SIZE: int = 4



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader):
        """
        Creates a new {@link MultiPayloadEnumDescriptor}
        @param reader A {@link BinaryReader} positioned at the start of the structure
        @throws IOException if there was an IO-related problem creating the structure
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getBase(self) -> long:
        """
        Gets the base "address" of this {@link SwiftTypeMetadataStructure}
        @return The base "address" of this {@link SwiftTypeMetadataStructure}
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getContents(self) -> List[int]:
        """
        Gets the contents
        @return The contents
        """
        ...

    def getContentsSize(self) -> long:
        """
        Gets the size of the contents in bytes
        @return The size of the contents in bytes
        """
        ...

    def getDescription(self) -> unicode: ...

    def getStructureName(self) -> unicode: ...

    def getTypeName(self) -> unicode:
        """
        Gets the type name
        @return The type name
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
    def contents(self) -> List[int]: ...

    @property
    def contentsSize(self) -> long: ...

    @property
    def description(self) -> unicode: ...

    @property
    def structureName(self) -> unicode: ...

    @property
    def typeName(self) -> unicode: ...