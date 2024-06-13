from typing import List
from typing import overload
import ghidra.app.plugin.assembler.sleigh.expr
import ghidra.app.plugin.assembler.sleigh.sem
import ghidra.app.plugin.processors.sleigh
import java.lang
import java.util


class AssemblyResolvedPatterns(ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution, object):








    def backfill(self, solver: ghidra.app.plugin.assembler.sleigh.expr.RecursiveDescentSolver, vals: java.util.Map) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution:
        """
        Apply as many backfill records as possible
 
         <p>
         Each backfill record is resolved in turn, if the record cannot be resolved, it remains
         listed. If the record can be resolved, but it conflicts, an error record is returned. Each
         time a record is resolved and combined successfully, all remaining records are tried again.
         The result is the combined resolved backfills, with only the unresolved backfill records
         listed.
        @param solver the solver, usually the same as the original attempt to solve.
        @param vals the values.
        @return the result, or an error.
        """
        ...

    def bitsEqual(self, that: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns) -> bool:
        """
        Check if this and another resolution have equal encodings
 
         <p>
         This is like {@link Object#equals(Object)}, but it ignores backfill records and forbidden 
         patterns.
        @param that the other resolution
        @return true if both have equal encodings
        """
        ...

    def checkNotForbidden(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution:
        """
        Check if the current encoding is forbidden by one of the attached patterns
 
         <p>
         The pattern becomes forbidden if this encoding's known bits are an overset of any forbidden
         pattern's known bits.
        @return false if the pattern is forbidden (and thus in error), true if permitted
        """
        ...

    def collectAllRight(self, __a0: java.util.Collection) -> None: ...

    @overload
    def combine(self, bf: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedBackfill) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns:
        """
        Combine the given backfill record into this resolution
        @param bf the backfill record
        @return the result
        """
        ...

    @overload
    def combine(self, pat: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns:
        """
        Combine the encodings and backfills of the given resolution into this one
 
         <p>
         This combines corresponding pattern blocks (assuming they agree), collects backfill records,
         and collects forbidden patterns.
        @param pat the other resolution
        @return the result if successful, or null
        """
        ...

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

    def compareTo(self, __a0: object) -> int: ...

    def dumpConstructorTree(self) -> unicode:
        """
        Used for testing and diagnostics: list the constructor line numbers used to resolve this
         encoding
 
         <p>
         This includes braces to describe the tree structure
        @see ConstructState#dumpConstructorTree()
        @return the constructor tree
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def equivalentConstructState(self, state: ghidra.app.plugin.processors.sleigh.ConstructState) -> bool:
        """
        Check if this assembled construct state is the same as the given dis-assembled construct
         state.
        """
        ...

    def getBackfills(self) -> java.util.Collection:
        """
        Get the backfill records for this resolution, if any
        @return the backfills
        """
        ...

    def getChildren(self) -> List[object]: ...

    def getClass(self) -> java.lang.Class: ...

    def getContext(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Get the context block
        @return the context block
        """
        ...

    def getDefinedInstructionLength(self) -> int:
        """
        Get the length of the instruction encoding, excluding trailing undefined bytes
 
         <p>
         <b>NOTE:</b> this DOES include the offset<br>
         <b>NOTE:</b> this DOES NOT include pending backfills
        @return the length of the defined bytes in the instruction block
        """
        ...

    def getDescription(self) -> unicode: ...

    def getForbids(self) -> java.util.Collection:
        """
        Get the forbidden patterns for this resolution
 
         <p>
         These represent patterns included in the current resolution that would actually get matched
         by a more specific constructor somewhere in the resolved tree, and thus are subtracted.
        @return the forbidden patterns
        """
        ...

    def getInstruction(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock:
        """
        Get the instruction block
        @return the instruction block
        """
        ...

    def getInstructionLength(self) -> int:
        """
        Get the length of the instruction encoding
 
         <p>
         This is used to ensure each operand is encoded at the correct offset
 
         <p>
         <b>NOTE:</b> this DOES include the offset<br>
         <b>NOTE:</b> this DOES include pending backfills
        @return the length of the instruction block
        """
        ...

    def getRight(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

    def hasBackfills(self) -> bool:
        """
        Check if this resolution has pending backfills to apply
        @return true if there are backfills
        """
        ...

    def hasChildren(self) -> bool: ...

    def hashCode(self) -> int: ...

    def isBackfill(self) -> bool: ...

    def isError(self) -> bool: ...

    def lineToString(self) -> unicode: ...

    def maskOut(self, cop: ghidra.app.plugin.processors.sleigh.ContextOp) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns:
        """
        Set all bits read by a given context operation to unknown
        @param cop the context operation
        @return the result
        @see AssemblyPatternBlock#maskOut(ContextOp)
        """
        ...

    def nopLeftSibling(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns:
        """
        Generate a new nop right this resolution to its right.
 
         <p>
         Alternatively phrased: append a nop to the left of this list of siblings, returning the new
         head.
        @return the nop resolution
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parent(self, description: unicode, opCount: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    def possibleInsVals(self, forCtx: ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock) -> List[java.lang.Iterable]:
        """
        Get an iterable over all the possible fillings of the instruction pattern given a context
 
         <p>
         This is meant to be used idiomatically, as in an enhanced for loop:
 
         <pre>
         for (byte[] ins : rcon.possibleInsVals(ctx)) {
         	System.out.println(format(ins));
         }
         </pre>
 
         <p>
         This is similar to calling
         {@link #getInstruction()}.{@link AssemblyPatternBlock#possibleVals()}, <em>but</em> with
         forbidden patterns removed. A context is required so that only those forbidden patterns
         matching the given context are actually removed. This method should always be preferred to
         the sequence mentioned above, since {@link AssemblyPatternBlock#possibleVals()} on its own
         may yield bytes that do not produce the desired instruction.
 
         <p>
         <b>NOTE:</b> The implementation is based on {@link AssemblyPatternBlock#possibleVals()}, so
         be aware that a single array is reused for each iterate. You should not retain a pointer to
         the array, but rather make a copy.
        @param forCtx the context at the assembly address
        @return the iterable
        """
        ...

    def readContext(self, start: int, len: int) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong:
        """
        Decode a portion of the context block
        @param start the first byte to decode
        @param len the number of bytes to decode
        @return the read masked value
        @see AssemblyPatternBlock#readBytes(int, int)
        """
        ...

    def readContextOp(self, cop: ghidra.app.plugin.processors.sleigh.ContextOp) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong:
        """
        Decode the value from the context located where the given context operation would write
 
         <p>
         This is used to read the value from the left-hand-side "variable" of a context operation. It
         seems backward, because it is. When assembling, the right-hand-side expression of a context
         operation must be solved. This means the "variable" is known from the context(s) of the
         resolved children constructors. The value read is then used as the goal in solving the
         expression.
        @param cop the context operation whose "variable" to read.
        @return the masked result.
        """
        ...

    def readInstruction(self, byteStart: int, size: int) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong:
        """
        Decode a portion of the instruction block
        @param byteStart the first byte to decode
        @param size the number of bytes to decode
        @return the read masked value
        @see AssemblyPatternBlock#readBytes(int, int)
        """
        ...

    def shift(self, shamt: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    def solveContextChangesForForbids(self, sem: ghidra.app.plugin.assembler.sleigh.sem.AssemblyConstructorSemantic, vals: java.util.Map) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns:
        """
        Solve and apply context changes in reverse to forbidden patterns
 
         <p>
         To avoid circumstances where a context change during disassembly would invoke a more specific
         sub-constructor than was used to assembly the instruction, we must solve the forbidden
         patterns in tandem with the overall resolution. If the context of any forbidden pattern
         cannot be solved, we simply drop the forbidden pattern -- the lack of a solution implies
         there is no way the context change could produce the forbidden pattern.
        @param sem the constructor whose context changes to solve
        @param vals any defined symbols
        @return the result
        @see AssemblyConstructorSemantic#solveContextChanges(AssemblyResolvedPatterns, Map)
        """
        ...

    @overload
    def toString(self) -> unicode: ...

    @overload
    def toString(self, __a0: unicode) -> unicode: ...

    def truncate(self, shamt: int) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns:
        """
        Truncate (unshift) the resolved instruction pattern from the left
 
         <b>NOTE:</b> This drops all backfill and forbidden pattern records, since this method is
         typically used to read token fields rather than passed around for resolution.
        @param shamt the number of bytes to remove from the left
        @return the result
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def withConstructor(self, cons: ghidra.app.plugin.processors.sleigh.Constructor) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns:
        """
        Create a copy of this resolution with a replaced constructor
        @param cons the new constructor
        @return the copy
        """
        ...

    def withDescription(self, description: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns:
        """
        Create a copy of this resolution with a new description
        @param description the new description
        @return the copy
        """
        ...

    def withForbids(self, more: java.util.Set) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns:
        """
        Create a new resolution from this one with the given forbidden patterns recorded
        @param more the additional forbidden patterns to record
        @return the new resolution
        """
        ...

    def withRight(self, right: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns:
        """
        Create a copy of this resolution with a sibling to the right
 
         <p>
         The right sibling is a mechanism for collecting children of a parent yet to be created. See
         {@link #parent(String, int)}.
        @param right the right sibling
        @return the new resolution
        """
        ...

    def writeContextOp(self, cop: ghidra.app.plugin.processors.sleigh.ContextOp, val: ghidra.app.plugin.assembler.sleigh.expr.MaskedLong) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns:
        """
        Encode the given value into the context block as specified by an operation
 
         <p>
         This is the forward (as in disassembly) direction of applying context operations. The pattern
         expression is evaluated, and the result is written as specified.
        @param cop the context operation specifying the location of the value to encode
        @param val the masked value to encode
        @return the result
        """
        ...

    @property
    def backfills(self) -> java.util.Collection: ...

    @property
    def children(self) -> List[object]: ...

    @property
    def context(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock: ...

    @property
    def definedInstructionLength(self) -> int: ...

    @property
    def description(self) -> unicode: ...

    @property
    def error(self) -> bool: ...

    @property
    def forbids(self) -> java.util.Collection: ...

    @property
    def instruction(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock: ...

    @property
    def instructionLength(self) -> int: ...

    @property
    def right(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...