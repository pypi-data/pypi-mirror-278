from typing import List
from typing import overload
import ghidra.app.plugin.assembler.sleigh.sem
import java.lang
import java.util


class AbstractAssemblyResolution(object, ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution):
    """
    The (often intermediate) result of assembly
 
 
     These may represent a successful construction (AssemblyResolvedPatterns, a future field
     (AssemblyResolvedBackfill), or an error (AssemblyResolvedError).
 
 
     This class also provides the static factory methods for constructing any of its subclasses.
    """









    def collectAllRight(self, into: java.util.Collection) -> None: ...

    @overload
    def compareTo(self, that: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def equals(self, __a0: object) -> bool: ...

    def getChildren(self) -> List[ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution]: ...

    def getClass(self) -> java.lang.Class: ...

    def getDescription(self) -> unicode: ...

    def getRight(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

    def hasChildren(self) -> bool: ...

    def hashCode(self) -> int: ...

    def isBackfill(self) -> bool: ...

    def isError(self) -> bool: ...

    def lineToString(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parent(self, __a0: unicode, __a1: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

    def shift(self, amt: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

    @overload
    def toString(self) -> unicode: ...

    @overload
    def toString(self, indent: unicode) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def withRight(self, right: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution:
        """
        Get this same resolution, but with the given right sibling
        @param right the right sibling
        @return the resolution
        """
        ...

    def withoutRight(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution:
        """
        Get this same resolution, but without any right siblings
        @return the resolution
        """
        ...

    @property
    def backfill(self) -> bool: ...

    @property
    def children(self) -> List[object]: ...

    @property
    def description(self) -> unicode: ...

    @property
    def error(self) -> bool: ...

    @property
    def right(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...