from typing import overload
import ghidra.app.util.bin.format.pdb2.pdbreader
import ghidra.app.util.pdb.pdbapplicator
import java.lang


class ComplexTypeMapper(object):




    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getMapped(self, __a0: ghidra.app.util.bin.format.pdb2.pdbreader.RecordNumber) -> ghidra.app.util.bin.format.pdb2.pdbreader.RecordNumber: ...

    def hashCode(self) -> int: ...

    def mapTypes(self, __a0: ghidra.app.util.pdb.pdbapplicator.PdbApplicator) -> None: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

