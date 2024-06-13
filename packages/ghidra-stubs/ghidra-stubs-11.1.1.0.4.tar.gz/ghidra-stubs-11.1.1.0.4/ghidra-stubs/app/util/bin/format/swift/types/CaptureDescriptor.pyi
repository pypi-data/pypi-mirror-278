from typing import List
from typing import overload
import ghidra.app.util.bin.format.swift
import ghidra.app.util.bin.format.swift.types
import ghidra.program.model.data
import java.lang


class CaptureDescriptor(ghidra.app.util.bin.format.swift.SwiftTypeMetadataStructure):
    """
    Represents a Swift CaptureDescriptor structure
    """

    SIZE: int = 12



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader):
        """
        Creates a new {@link CaptureDescriptor}
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

    def getCaptureTypeRecords(self) -> List[ghidra.app.util.bin.format.swift.types.CaptureTypeRecord]:
        """
        Gets the {@link List} of {@link CaptureTypeRecord}s
        @return The {@link List} of {@link CaptureTypeRecord}s
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getDescription(self) -> unicode: ...

    def getMetadataSourceRecords(self) -> List[ghidra.app.util.bin.format.swift.types.MetadataSourceRecord]:
        """
        Gets the {@link List} of {@link MetadataSourceRecord}s
        @return The {@link List} of {@link MetadataSourceRecord}s
        """
        ...

    def getNumBindings(self) -> int:
        """
        Gets the number of bindings
        @return The number of bindings
        """
        ...

    def getNumCaptureTypes(self) -> int:
        """
        Gets the number of capture types
        @return The number of capture types
        """
        ...

    def getNumMetadataSources(self) -> int:
        """
        Gets the number of metadata sources
        @return The number of metadata sources
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
    def captureTypeRecords(self) -> List[object]: ...

    @property
    def description(self) -> unicode: ...

    @property
    def metadataSourceRecords(self) -> List[object]: ...

    @property
    def numBindings(self) -> int: ...

    @property
    def numCaptureTypes(self) -> int: ...

    @property
    def numMetadataSources(self) -> int: ...

    @property
    def structureName(self) -> unicode: ...