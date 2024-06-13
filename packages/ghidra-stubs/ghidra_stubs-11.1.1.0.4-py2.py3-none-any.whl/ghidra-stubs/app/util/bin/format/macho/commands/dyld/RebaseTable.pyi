from typing import List
from typing import overload
import ghidra.app.util.bin.format.macho.commands.dyld
import ghidra.app.util.bin.format.macho.commands.dyld.RebaseTable
import java.lang


class RebaseTable(ghidra.app.util.bin.format.macho.commands.dyld.OpcodeTable):
    """
    A Mach-O rebase table
    """






    class Rebase(object):




        @overload
        def __init__(self): ...

        @overload
        def __init__(self, __a0: ghidra.app.util.bin.format.macho.commands.dyld.RebaseTable.Rebase): ...



        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getSegmentIndex(self) -> int: ...

        def getSegmentOffset(self) -> long: ...

        def getType(self) -> int: ...

        def getUnknownOpcode(self) -> int: ...

        def hashCode(self) -> int: ...

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
        def segmentIndex(self) -> int: ...

        @property
        def segmentOffset(self) -> long: ...

        @property
        def type(self) -> int: ...

        @property
        def unknownOpcode(self) -> int: ...

    @overload
    def __init__(self):
        """
        Creates an empty {@link RebaseTable}
        """
        ...

    @overload
    def __init__(self, reader: ghidra.app.util.bin.BinaryReader, header: ghidra.app.util.bin.format.macho.MachHeader, tableSize: int):
        """
        Creates and parses a new {@link RebaseTable}
        @param reader A {@link BinaryReader reader} positioned at the start of the rebase table
        @param header The header
        @param tableSize The size of the table, in bytes
        @throws IOException if an IO-related error occurs while parsing
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getOpcodeOffsets(self) -> List[long]:
        """
        {@return opcode offsets from the start of the bind data}
        """
        ...

    def getRebases(self) -> List[ghidra.app.util.bin.format.macho.commands.dyld.RebaseTable.Rebase]:
        """
        {@return the rebases}
        """
        ...

    def getSlebOffsets(self) -> List[long]:
        """
        {@return SLEB128 offsets from the start of the bind data}
        """
        ...

    def getStringOffsets(self) -> List[long]:
        """
        {@return string offsets from the start of the bind data}
        """
        ...

    def getUlebOffsets(self) -> List[long]:
        """
        {@return ULEB128 offsets from the start of the bind data}
        """
        ...

    def hashCode(self) -> int: ...

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
    def rebases(self) -> List[object]: ...