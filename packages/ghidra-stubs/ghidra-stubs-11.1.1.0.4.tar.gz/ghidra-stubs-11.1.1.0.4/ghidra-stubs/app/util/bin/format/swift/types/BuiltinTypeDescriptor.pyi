from typing import overload
import ghidra.app.util.bin.format.swift
import ghidra.program.model.data
import java.lang


class BuiltinTypeDescriptor(ghidra.app.util.bin.format.swift.SwiftTypeMetadataStructure):
    """
    Represents a Swift BuiltinTypeDescriptor structure
    """

    SIZE: int = 20



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader):
        """
        Creates a new {@link BuiltinTypeDescriptor}
        @param reader A {@link BinaryReader} positioned at the start of the structure
        @throws IOException if there was an IO-related problem creating the structure
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getAlignmentAndFlags(self) -> int:
        """
        Gets the alignment and flags
        @return The alignment and flags
        """
        ...

    def getBase(self) -> long:
        """
        Gets the base "address" of this {@link SwiftTypeMetadataStructure}
        @return The base "address" of this {@link SwiftTypeMetadataStructure}
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getDescription(self) -> unicode: ...

    def getNumExtraInhabitants(self) -> int:
        """
        Gets the number of extra inhabitants
        @return The number of extra inhabitants
        """
        ...

    def getSize(self) -> int:
        """
        Gets the size
        @return The size
        """
        ...

    def getStride(self) -> int:
        """
        Gets the stride
        @return The stride
        """
        ...

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
    def alignmentAndFlags(self) -> int: ...

    @property
    def description(self) -> unicode: ...

    @property
    def numExtraInhabitants(self) -> int: ...

    @property
    def size(self) -> int: ...

    @property
    def stride(self) -> int: ...

    @property
    def structureName(self) -> unicode: ...

    @property
    def typeName(self) -> unicode: ...