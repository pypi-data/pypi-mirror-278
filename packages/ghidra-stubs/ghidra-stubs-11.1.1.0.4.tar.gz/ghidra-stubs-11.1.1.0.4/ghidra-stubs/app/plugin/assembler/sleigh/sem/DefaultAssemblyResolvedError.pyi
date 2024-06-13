from typing import List
from typing import overload
import ghidra.app.plugin.assembler.sleigh.sem
import java.lang
import java.util


class DefaultAssemblyResolvedError(ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolution, ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedError):
    """
    A AssemblyResolution indicating the occurrence of a (usually semantic) error
 
 
     The description should indicate where the error occurred. The error message should explain the
     actual error. To help the user diagnose the nature of the error, errors in sub-constructors
     should be placed as children of an error given by the parent constructor.
    """









    def collectAllRight(self, into: java.util.Collection) -> None: ...

    @overload
    def compareTo(self, that: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def equals(self, obj: object) -> bool: ...

    def getChildren(self) -> List[ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution]: ...

    def getClass(self) -> java.lang.Class: ...

    def getDescription(self) -> unicode: ...

    def getError(self) -> unicode:
        """
        Get a description of the error
        @return the description
        """
        ...

    def getRight(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

    def hasChildren(self) -> bool: ...

    def hashCode(self) -> int: ...

    def isBackfill(self) -> bool: ...

    def isError(self) -> bool: ...

    def lineToString(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parent(self, description: unicode, opCount: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

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

    def withRight(self, right: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

    def withoutRight(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution:
        """
        Get this same resolution, but without any right siblings
        @return the resolution
        """
        ...

    @property
    def backfill(self) -> bool: ...

    @property
    def error(self) -> bool: ...