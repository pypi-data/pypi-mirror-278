from typing import List
from typing import overload
import ghidra.app.plugin.assembler.sleigh.expr
import ghidra.app.plugin.assembler.sleigh.sem
import java.lang
import java.util


class AssemblyResolvedBackfill(ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution, object):








    def collectAllRight(self, __a0: java.util.Collection) -> None: ...

    def compareTo(self, __a0: object) -> int: ...

    def equals(self, __a0: object) -> bool: ...

    def getChildren(self) -> List[object]: ...

    def getClass(self) -> java.lang.Class: ...

    def getDescription(self) -> unicode: ...

    def getInstructionLength(self) -> int:
        """
        Get the expected length of the instruction portion of the future encoding
 
         This is used to make sure that operands following a to-be-determined encoding are placed
         properly. Even though the actual encoding cannot yet be determined, its length can.
        @return the total expected length (including the offset)
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

    def parent(self, __a0: unicode, __a1: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

    def shift(self, amt: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedBackfill: ...

    def solve(self, solver: ghidra.app.plugin.assembler.sleigh.expr.RecursiveDescentSolver, vals: java.util.Map, cur: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution:
        """
        Attempt (again) to solve the expression that generated this backfill record
 
         <p>
         This will attempt to solve the same expression and goal again, using the same parameters as
         were given to the original attempt, except with additional defined symbols. Typically, the
         symbol that required backfill is {@code inst_next}. This method will not throw
         {@link NeedsBackfillException}, since that would imply the missing symbol(s) from the
         original attempt are still missing. Instead, the method returns an instance of
         {@link AssemblyResolvedError}.
        @param solver a solver, usually the same as the one from the original attempt.
        @param vals the defined symbols, usually the same, but with the missing symbol(s).
        @return the solution result
        """
        ...

    @overload
    def toString(self) -> unicode: ...

    @overload
    def toString(self, __a0: unicode) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def backfill(self) -> bool: ...

    @property
    def children(self) -> List[object]: ...

    @property
    def description(self) -> unicode: ...

    @property
    def error(self) -> bool: ...

    @property
    def instructionLength(self) -> int: ...

    @property
    def right(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...