from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.macho.commands.chained
import ghidra.app.util.bin.format.macho.dyld
import ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr
import ghidra.app.util.importer
import ghidra.program.model.address
import ghidra.program.model.listing
import ghidra.program.model.symbol
import ghidra.util.task
import java.lang


class DyldChainedFixups(object):




    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def fixupChainedPointers(__a0: List[object], __a1: ghidra.program.model.listing.Program, __a2: ghidra.program.model.address.Address, __a3: List[object], __a4: ghidra.app.util.importer.MessageLog, __a5: ghidra.util.task.TaskMonitor) -> List[object]: ...

    @staticmethod
    def getChainedFixups(reader: ghidra.app.util.bin.BinaryReader, chainedImports: ghidra.app.util.bin.format.macho.commands.chained.DyldChainedImports, pointerFormat: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType, page: long, nextOff: long, auth_value_add: long, imagebase: long, symbolTable: ghidra.program.model.symbol.SymbolTable, log: ghidra.app.util.importer.MessageLog, monitor: ghidra.util.task.TaskMonitor) -> List[ghidra.app.util.bin.format.macho.dyld.DyldFixup]:
        """
        Walks the chained fixup information and collects a {@link List} of {@link DyldFixup}s that 
         will need to be applied to the image
        @param reader A {@link BinaryReader} that can read the image
        @param chainedImports chained imports (could be null)
        @param pointerFormat format of pointers within this chain
        @param page within data pages that has pointers to be unchained
        @param nextOff offset within the page that is the chain start
        @param auth_value_add value to be added to each chain pointer
        @param imagebase The image base
        @param symbolTable The {@link SymbolTable}, or null if not available
        @param log The log
        @param monitor A cancellable monitor
        @return A {@link List} of {@link DyldFixup}s
        @throws IOException If there was an IO-related issue
        @throws CancelledException If the user cancelled the operation
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def processPointerChain(reader: ghidra.app.util.bin.BinaryReader, chainStart: long, nextOffSize: long, imagebase: long, log: ghidra.app.util.importer.MessageLog, monitor: ghidra.util.task.TaskMonitor) -> List[ghidra.app.util.bin.format.macho.dyld.DyldFixup]:
        """
        Fixes up any chained pointers, starting at the given address.
        @param reader A {@link BinaryReader} that can read the image
        @param chainStart The starting of address of the pointer chain to fix.
        @param nextOffSize The size of the next offset.
        @param imagebase The image base
        @param log The log
        @param monitor A cancellable monitor
        @return A list of addresses where pointer fixes were performed.
        @throws IOException If there was an IO-related issue
        @throws CancelledException If the user cancelled the operation
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

