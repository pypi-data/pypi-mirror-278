from typing import List
from typing import overload
import ghidra.app.util.bin.format.swift
import ghidra.app.util.bin.format.swift.types
import ghidra.program.model.data
import java.lang


class AssociatedTypeDescriptor(ghidra.app.util.bin.format.swift.SwiftTypeMetadataStructure):
    """
    Represents a Swift AssociatedTypeDescriptor structure
    """

    SIZE: int = 16



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader):
        """
        Creates a new {@link AssociatedTypeDescriptor}
        @param reader A {@link BinaryReader} positioned at the start of the structure
        @throws IOException if there was an IO-related problem creating the structure
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getAssociatedTypeRecordSize(self) -> int:
        """
        Gets the associated type record size
        @return The associated type record size
        """
        ...

    def getAssociatedTypeRecords(self) -> List[ghidra.app.util.bin.format.swift.types.AssociatedTypeRecord]:
        """
        Gets the {@link List} of {@link AssociatedTypeRecord}s
        @return The {@link List} of {@link AssociatedTypeRecord}s
        """
        ...

    def getBase(self) -> long:
        """
        Gets the base "address" of this {@link SwiftTypeMetadataStructure}
        @return The base "address" of this {@link SwiftTypeMetadataStructure}
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getConformingTypeName(self) -> unicode:
        """
        Gets the conforming type name
        @return The conforming type name
        """
        ...

    def getDescription(self) -> unicode: ...

    def getNumAssociatedTypes(self) -> int:
        """
        Gets the number of associated types
        @return The number of associated types
        """
        ...

    def getProtocolTypeName(self) -> unicode:
        """
        Gets the protocol type name
        @return The protocol type name
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
    def associatedTypeRecordSize(self) -> int: ...

    @property
    def associatedTypeRecords(self) -> List[object]: ...

    @property
    def conformingTypeName(self) -> unicode: ...

    @property
    def description(self) -> unicode: ...

    @property
    def numAssociatedTypes(self) -> int: ...

    @property
    def protocolTypeName(self) -> unicode: ...

    @property
    def structureName(self) -> unicode: ...