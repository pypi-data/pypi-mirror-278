from typing import overload
import ghidra.app.util.bin.format.pdb2.pdbreader
import ghidra.app.util.pdb.pdbapplicator
import java.lang


class EndSymbolApplier(ghidra.app.util.pdb.pdbapplicator.MsSymbolApplier, ghidra.app.util.pdb.pdbapplicator.BlockNestingSymbolApplier, ghidra.app.util.pdb.pdbapplicator.NestableSymbolApplier):




    def __init__(self, __a0: ghidra.app.util.pdb.pdbapplicator.DefaultPdbApplicator, __a1: ghidra.app.util.bin.format.pdb2.pdbreader.symbol.EndMsSymbol): ...



    def applyTo(self, __a0: ghidra.app.util.pdb.pdbapplicator.NestingSymbolApplier, __a1: ghidra.app.util.bin.format.pdb2.pdbreader.MsSymbolIterator) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

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

