from typing import overload
import ghidra.app.util.bin.format.swift
import ghidra.program.model.data
import java.lang


class FieldRecord(ghidra.app.util.bin.format.swift.SwiftTypeMetadataStructure):
    """
    Represents a Swift FieldRecord structure
    """

    SIZE: int = 12



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader):
        """
        Creates a new {@link FieldRecord}
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

    def getDescription(self) -> unicode: ...

    def getFieldName(self) -> unicode:
        """
        Gets the field name
        @return The field name
        """
        ...

    def getFlags(self) -> int:
        """
        Gets the flags
        @return The flags
        """
        ...

    def getMangledTypeName(self) -> unicode:
        """
        Gets the mangled type name
        @return The mangled type name
        """
        ...

    def getStructureName(self) -> unicode: ...

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
    def description(self) -> unicode: ...

    @property
    def fieldName(self) -> unicode: ...

    @property
    def flags(self) -> int: ...

    @property
    def mangledTypeName(self) -> unicode: ...

    @property
    def structureName(self) -> unicode: ...