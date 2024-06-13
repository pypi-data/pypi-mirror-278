from typing import overload
import ghidra.app.util.pdb.pdbapplicator
import java.lang


class ClassFieldAttributes(object):
    BLANK: ghidra.app.util.pdb.pdbapplicator.ClassFieldAttributes
    UNKNOWN: ghidra.app.util.pdb.pdbapplicator.ClassFieldAttributes







    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def get(__a0: ghidra.app.util.pdb.pdbapplicator.ClassFieldAttributes.Access, __a1: ghidra.app.util.pdb.pdbapplicator.ClassFieldAttributes.Property) -> ghidra.app.util.pdb.pdbapplicator.ClassFieldAttributes: ...

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

