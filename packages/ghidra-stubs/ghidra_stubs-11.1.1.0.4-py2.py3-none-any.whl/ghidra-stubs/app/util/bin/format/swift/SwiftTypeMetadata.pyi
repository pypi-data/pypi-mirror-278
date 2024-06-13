from typing import List
from typing import overload
import ghidra.app.util.bin.format.swift.types
import java.lang
import java.util


class SwiftTypeMetadata(object):
    """
    Parses marks up, and provide access to Swift type metadata
    """





    def __init__(self, program: ghidra.program.model.listing.Program, monitor: ghidra.util.task.TaskMonitor, log: ghidra.app.util.importer.MessageLog):
        """
        Creates a new {@link SwiftTypeMetadata}
        @param program The {@link Program}
        @param monitor A cancellable task monitor
        @param log The log
        @throws IOException if there was an IO-related error
        @throws CancelledException if the user cancelled the operation
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getAssociatedTypeDescriptor(self) -> List[ghidra.app.util.bin.format.swift.types.AssociatedTypeDescriptor]:
        """
        {@return the associated type descriptors}
        """
        ...

    def getBuiltinTypeDescriptors(self) -> List[ghidra.app.util.bin.format.swift.types.BuiltinTypeDescriptor]:
        """
        {@return the built-in type descriptors}
        """
        ...

    def getCaptureDescriptors(self) -> List[ghidra.app.util.bin.format.swift.types.CaptureDescriptor]:
        """
        {@return the capture descriptors}
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getEntryPoints(self) -> List[ghidra.app.util.bin.format.swift.types.EntryPoint]:
        """
        {@return the entry points}
        """
        ...

    def getFieldDescriptors(self) -> java.util.Map:
        """
        {@return the field descriptors}
        """
        ...

    def getMultiPayloadEnumDescriptors(self) -> List[ghidra.app.util.bin.format.swift.types.MultiPayloadEnumDescriptor]:
        """
        {@return the multi-payload enum descriptors}
        """
        ...

    def getTargetProtocolConformanceDescriptors(self) -> List[ghidra.app.util.bin.format.swift.types.TargetProtocolConformanceDescriptor]:
        """
        {@return the target protocol conformance descriptors}
        """
        ...

    def getTargetProtocolDescriptors(self) -> List[ghidra.app.util.bin.format.swift.types.TargetProtocolDescriptor]:
        """
        {@return the target protocol descriptors}
        """
        ...

    def getTargetTypeContextDescriptors(self) -> java.util.Map:
        """
        {@return the type descriptors}
        """
        ...

    def hashCode(self) -> int: ...

    def markup(self) -> None:
        """
        Marks up this {@link SwiftTypeMetadata} with data structures and comments
        @throws CancelledException if the user cancelled the operation
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def associatedTypeDescriptor(self) -> List[object]: ...

    @property
    def builtinTypeDescriptors(self) -> List[object]: ...

    @property
    def captureDescriptors(self) -> List[object]: ...

    @property
    def entryPoints(self) -> List[object]: ...

    @property
    def fieldDescriptors(self) -> java.util.Map: ...

    @property
    def multiPayloadEnumDescriptors(self) -> List[object]: ...

    @property
    def targetProtocolConformanceDescriptors(self) -> List[object]: ...

    @property
    def targetProtocolDescriptors(self) -> List[object]: ...

    @property
    def targetTypeContextDescriptors(self) -> java.util.Map: ...