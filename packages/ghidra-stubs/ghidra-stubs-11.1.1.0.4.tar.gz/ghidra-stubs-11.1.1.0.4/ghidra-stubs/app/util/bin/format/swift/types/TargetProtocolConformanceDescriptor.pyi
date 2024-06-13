from typing import overload
import ghidra.app.util.bin.format.swift
import ghidra.program.model.data
import java.lang


class TargetProtocolConformanceDescriptor(ghidra.app.util.bin.format.swift.SwiftTypeMetadataStructure):
    """
    Represents a Swift TargetProtocolConformanceDescriptor structure
    """





    def __init__(self, reader: ghidra.app.util.bin.BinaryReader):
        """
        Creates a new {@link TargetProtocolConformanceDescriptor}
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

    def getConformanceFlags(self) -> int:
        """
        Gets various flags, including the kind of conformance
        @return Various flags, including the kind of conformance
        """
        ...

    def getDescription(self) -> unicode: ...

    def getNominalTypeDescriptor(self) -> int:
        """
        Gets some description of the type that conforms to the protocol
        @return Some description of the type that conforms to the protocol
        """
        ...

    def getProtocolDescriptor(self) -> int:
        """
        Gets the protocol being conformed to
        @return The protocol being conformed to
        """
        ...

    def getProtocolWitnessTable(self) -> int:
        """
        Gets the witness table pattern, which may also serve as the witness table
        @return The witness table pattern, which may also serve as the witness table
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
    def conformanceFlags(self) -> int: ...

    @property
    def description(self) -> unicode: ...

    @property
    def nominalTypeDescriptor(self) -> int: ...

    @property
    def protocolDescriptor(self) -> int: ...

    @property
    def protocolWitnessTable(self) -> int: ...

    @property
    def structureName(self) -> unicode: ...