from typing import overload
import ghidra.app.util.bin.format.swift.types
import ghidra.program.model.data
import java.lang
import java.util


class TargetTypeContextDescriptor(ghidra.app.util.bin.format.swift.types.TargetContextDescriptor):
    """
    Represents a Swift TargetTypeContextDescriptor structure
    """





    def __init__(self, reader: ghidra.app.util.bin.BinaryReader):
        """
        Creates a new {@link TargetTypeContextDescriptor}
        @param reader A {@link BinaryReader} positioned at the start of the structure
        @throws IOException if there was an IO-related problem creating the structure
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getAccessFunctionPtr(self) -> int:
        """
        Gets the pointer to the metadata access function for this type
        @return The pointer to the metadata access function for this type
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

    def getFieldDescriptor(self, fieldDescriptors: java.util.Map) -> ghidra.app.util.bin.format.swift.types.FieldDescriptor:
        """
        Gets this {@link TargetTypeContextDescriptor}'s {@link FieldDescriptor}
        @param fieldDescriptors A {@link Map} of {@link FieldDescriptor}'s keyed by their base
           addresses
        @return This {@link TargetTypeContextDescriptor}'s {@link FieldDescriptor}, or null if it
           doesn't have one
        """
        ...

    def getFields(self) -> int:
        """
        Gets the pointer to the field descriptor for the type, if any
        @return The pointer to the field descriptor for the type, if any
        """
        ...

    def getFlags(self) -> int:
        """
        Gets the flags
        @return The flags
        """
        ...

    def getName(self) -> unicode:
        """
        Gets the name of the type
        @return The name of the type
        """
        ...

    def getParent(self) -> int:
        """
        Gets the parent's relative offset
        @return The parent's relative offset
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
    def accessFunctionPtr(self) -> int: ...

    @property
    def description(self) -> unicode: ...

    @property
    def fields(self) -> int: ...

    @property
    def name(self) -> unicode: ...

    @property
    def structureName(self) -> unicode: ...