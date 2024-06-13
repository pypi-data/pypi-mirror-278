from typing import List
from typing import overload
import ghidra.app.plugin.assembler.sleigh.expr
import ghidra.app.plugin.assembler.sleigh.sem
import ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory
import ghidra.app.plugin.processors.sleigh
import ghidra.app.plugin.processors.sleigh.expression
import ghidra.app.plugin.processors.sleigh.pattern
import java.lang


class AbstractAssemblyResolutionFactory(object):





    class AbstractAssemblyResolutionBuilder(object):




        def __init__(self): ...



        def children(self, __a0: List[object]) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        def copyFromDefault(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolution) -> None: ...

        def description(self, __a0: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def right(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class AbstractAssemblyResolvedPatternsBuilder(ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder):




        def __init__(self): ...



        def children(self, __a0: List[object]) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        @overload
        def copyFromDefault(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.DefaultAssemblyResolvedPatterns) -> None: ...

        @overload
        def copyFromDefault(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolution) -> None: ...

        def description(self, __a0: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def right(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class DefaultAssemblyResolvedBackfillBuilder(ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolvedBackfillBuilder):




        def __init__(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory): ...



        def children(self, __a0: List[object]) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        def copyFromDefault(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolution) -> None: ...

        def description(self, __a0: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def right(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class AssemblyResolvedErrorBuilder(ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder):




        def __init__(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory): ...



        def build(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

        def children(self, __a0: List[object]) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        def copyFromDefault(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolution) -> None: ...

        def description(self, __a0: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        def equals(self, __a0: object) -> bool: ...

        def error(self, __a0: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AssemblyResolvedErrorBuilder: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def right(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class AbstractAssemblyResolvedBackfillBuilder(ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder):




        def __init__(self): ...



        def children(self, __a0: List[object]) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        def copyFromDefault(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolution) -> None: ...

        def description(self, __a0: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def right(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class DefaultAssemblyResolvedPatternBuilder(ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolvedPatternsBuilder):




        def __init__(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory): ...



        def children(self, __a0: List[object]) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        @overload
        def copyFromDefault(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.DefaultAssemblyResolvedPatterns) -> None: ...

        @overload
        def copyFromDefault(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolution) -> None: ...

        def description(self, __a0: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def right(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolutionBuilder: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...



    def __init__(self): ...



    def backfill(self, exp: ghidra.app.plugin.processors.sleigh.expression.PatternExpression, goal: ghidra.app.plugin.assembler.sleigh.expr.MaskedLong, inslen: int, description: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution:
        """
        Build a backfill record to attach to a successful resolution result
        @param exp the expression depending on a missing symbol
        @param goal the desired value of the expression
        @param inslen the length of instruction portion expected in the future solution
        @param description a description of the backfill record
        @return the new record
        """
        ...

    def backfillBuilder(self, exp: ghidra.app.plugin.processors.sleigh.expression.PatternExpression, goal: ghidra.app.plugin.assembler.sleigh.expr.MaskedLong, inslen: int, description: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolvedBackfillBuilder: ...

    def contextOnly(self, ctx: ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock, description: unicode) -> RP:
        """
        Build a context-only successful resolution result
        @param ctx the context pattern block
        @param description a description of the resolution
        @return the new resolution
        @see #resolved(AssemblyPatternBlock, AssemblyPatternBlock, String, Constructor, List,
              AssemblyResolution)
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def error(self, error: unicode, res: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution:
        """
        Build an error resolution record, based on an intermediate SLEIGH constructor record
        @param error a description of the error
        @param res the constructor record that was being populated when the error occurred
        @return the new error resolution
        """
        ...

    def errorBuilder(self, error: unicode, res: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory: ...

    def fromPattern(self, pat: ghidra.app.plugin.processors.sleigh.pattern.DisjointPattern, minLen: int, description: unicode, cons: ghidra.app.plugin.processors.sleigh.Constructor) -> RP:
        """
        Build a successful resolution result from a SLEIGH constructor's patterns
        @param pat the constructor's pattern
        @param description a description of the resolution
        @return the new resolution
        """
        ...

    def fromString(self, __a0: unicode, __a1: unicode, __a2: List[object]) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def instrOnly(self, ins: ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock, description: unicode) -> RP:
        """
        Build an instruction-only successful resolution result
        @param ins the instruction pattern block
        @param description a description of the resolution
        @return the new resolution
        @see #resolved(AssemblyPatternBlock, AssemblyPatternBlock, String, Constructor, List,
              AssemblyResolution)
        """
        ...

    def newAssemblyResolutionResults(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolutionResults: ...

    def newBackfillBuilder(self) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolvedBackfillBuilder: ...

    def newErrorBuilder(self) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory: ...

    def newPatternsBuilder(self) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory.AbstractAssemblyResolvedPatternsBuilder: ...

    @overload
    def nop(self, description: unicode) -> RP:
        """
        Obtain a new "blank" resolved SLEIGH constructor record
        @param description a description of the resolution
        @return the new resolution
        """
        ...

    @overload
    def nop(self, __a0: unicode, __a1: List[object], __a2: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def resolved(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock, __a1: ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock, __a2: unicode, __a3: ghidra.app.plugin.processors.sleigh.Constructor, __a4: List[object], __a5: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

