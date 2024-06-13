from typing import List
from typing import overload
import ghidra.app.plugin.assembler.sleigh.expr
import ghidra.app.plugin.assembler.sleigh.sem
import ghidra.app.plugin.processors.sleigh
import java.lang
import java.util


class DefaultAssemblyResolvedPatterns(ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolution, ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns):
    """
    A AssemblyResolution indicating successful application of a constructor
 
 
     This is almost analogous to ghidra.app.plugin.processors.sleigh.pattern.DisjointPattern, in that is joins an instruction AssemblyPatternBlock with a
     corresponding context AssemblyPatternBlock. However, this object is mutable, and it
     collects backfill records, as well as forbidden patterns.
 
 
     When the applied constructor is from the "instruction" subtable, this represents a fully-
     constructed instruction with required context. All backfill records ought to be resolved and
     applied before the final result is given to the user, i.e., passed into the
     AssemblySelector. If at any time during the resolution or backfill process, the result
     becomes confined to one of the forbidden patterns, it must be dropped, since the encoding will
     actually invoke a more specific SLEIGH constructor.
    """









    def backfill(self, solver: ghidra.app.plugin.assembler.sleigh.expr.RecursiveDescentSolver, vals: java.util.Map) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

    def bitsEqual(self, that: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns) -> bool: ...

    def checkNotForbidden(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

    def collectAllRight(self, into: java.util.Collection) -> None: ...

    @overload
    def combine(self, bf: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedBackfill) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    @overload
    def combine(self, that: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    def combineLessBackfill(self, that: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns, bf: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedBackfill) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns:
        """
        Combine a backfill result
 
         <p>
         When a backfill is successful, the result should be combined with the owning resolution. In
         addition, for bookkeeping's sake, the resolved record should be removed from the list of
         backfills.
        @param that the result from backfilling
        @param bf the resolved backfilled record
        @return the result if successful, or null
        """
        ...

    @overload
    def compareTo(self, that: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def copyAppendDescription(self, append: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns:
        """
        Duplicate this resolution, with additional description text appended
        @param append the text to append
        @return the duplicate NOTE: An additional separator {@code ": "} is inserted
        """
        ...

    def dumpConstructorTree(self) -> unicode: ...

    def equals(self, obj: object) -> bool: ...

    def equivalentConstructState(self, state: ghidra.app.plugin.processors.sleigh.ConstructState) -> bool: ...

    def getBackfills(self) -> java.util.Set: ...

    def getChildren(self) -> List[ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution]: ...

    def getClass(self) -> java.lang.Class: ...

    def getConstructor(self) -> ghidra.app.plugin.processors.sleigh.Constructor: ...

    def getContext(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock: ...

    def getDefinedInstructionLength(self) -> int: ...

    def getDescription(self) -> unicode: ...

    def getForbids(self) -> java.util.Set: ...

    def getInstruction(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock: ...

    def getInstructionLength(self) -> int: ...

    def getRight(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

    def getSpecificity(self) -> int:
        """
        Count the number of bits specified in the resolution patterns
 
         <p>
         Totals the specificity of the instruction and context pattern blocks.
        @return the number of bits in the resulting patterns
        @see AssemblyPatternBlock#getSpecificity()
        """
        ...

    def hasBackfills(self) -> bool: ...

    def hasChildren(self) -> bool: ...

    def hashCode(self) -> int: ...

    def isBackfill(self) -> bool: ...

    def isError(self) -> bool: ...

    def lineToString(self) -> unicode: ...

    def maskOut(self, cop: ghidra.app.plugin.processors.sleigh.ContextOp) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    def nopLeftSibling(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parent(self, description: unicode, opCount: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    def possibleInsVals(self, forCtx: ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock) -> List[java.lang.Iterable]: ...

    def readContext(self, start: int, len: int) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong: ...

    def readContextOp(self, cop: ghidra.app.plugin.processors.sleigh.ContextOp) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong: ...

    def readInstruction(self, start: int, len: int) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong: ...

    def shift(self, amt: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    def solveContextChangesForForbids(self, sem: ghidra.app.plugin.assembler.sleigh.sem.AssemblyConstructorSemantic, vals: java.util.Map) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    @overload
    def toString(self) -> unicode: ...

    @overload
    def toString(self, indent: unicode) -> unicode: ...

    def truncate(self, amt: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def withConstructor(self, cons: ghidra.app.plugin.processors.sleigh.Constructor) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    def withDescription(self, description: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    def withForbids(self, more: java.util.Set) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    def withRight(self, right: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    def withoutRight(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution:
        """
        Get this same resolution, but without any right siblings
        @return the resolution
        """
        ...

    def writeContextOp(self, cop: ghidra.app.plugin.processors.sleigh.ContextOp, val: ghidra.app.plugin.assembler.sleigh.expr.MaskedLong) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    @property
    def backfills(self) -> java.util.Set: ...

    @property
    def constructor(self) -> ghidra.app.plugin.processors.sleigh.Constructor: ...

    @property
    def context(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock: ...

    @property
    def definedInstructionLength(self) -> int: ...

    @property
    def error(self) -> bool: ...

    @property
    def forbids(self) -> java.util.Set: ...

    @property
    def instruction(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock: ...

    @property
    def instructionLength(self) -> int: ...

    @property
    def specificity(self) -> int: ...