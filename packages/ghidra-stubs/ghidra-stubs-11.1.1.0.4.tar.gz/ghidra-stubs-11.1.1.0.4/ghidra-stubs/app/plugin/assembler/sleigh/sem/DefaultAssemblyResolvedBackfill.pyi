from typing import List
from typing import overload
import ghidra.app.plugin.assembler.sleigh.expr
import ghidra.app.plugin.assembler.sleigh.sem
import java.lang
import java.util


class DefaultAssemblyResolvedBackfill(ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolution, ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedBackfill):
    """
    A AssemblyResolution indicating the need to solve an expression in the future
 
 
     Such records are collected within a AssemblyResolvedPatterns and then solved just before
     the final result(s) are assembled. This is typically required by instructions that refer to the
      symbol.
 
 
     NOTE: These are used internally. The user ought never to see these from the assembly API.
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

    def getInstructionLength(self) -> int: ...

    def getRight(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

    def hasChildren(self) -> bool: ...

    def hashCode(self) -> int: ...

    def isBackfill(self) -> bool: ...

    def isError(self) -> bool: ...

    def lineToString(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parent(self, description: unicode, opCount: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

    def shift(self, amt: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedBackfill: ...

    def solve(self, solver: ghidra.app.plugin.assembler.sleigh.expr.RecursiveDescentSolver, vals: java.util.Map, cur: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

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

    def withRight(self, right: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedBackfill: ...

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

    @property
    def instructionLength(self) -> int: ...