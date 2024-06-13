from typing import overload
import ghidra.app.plugin.assembler.sleigh.expr
import ghidra.app.plugin.assembler.sleigh.sem
import ghidra.app.plugin.processors.sleigh.expression
import java.lang
import java.util


class ContextFieldSolver(ghidra.app.plugin.assembler.sleigh.expr.AbstractExpressionSolver):
    """
    Solves expressions of a context register field
 
 
     Essentially, this just encodes the goal into the field, if it can be represented in the given
     space and format. Otherwise, there is no solution.
    """





    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @overload
    def getInstructionLength(self, cf: ghidra.app.plugin.processors.sleigh.expression.ContextField) -> int: ...

    @overload
    def getInstructionLength(self, __a0: ghidra.app.plugin.processors.sleigh.expression.PatternExpression) -> int: ...

    @overload
    def getValue(self, cf: ghidra.app.plugin.processors.sleigh.expression.ContextField, vals: java.util.Map, cur: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong: ...

    @overload
    def getValue(self, __a0: ghidra.app.plugin.processors.sleigh.expression.PatternExpression, __a1: java.util.Map, __a2: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    def solve(self, factory: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory, cf: ghidra.app.plugin.processors.sleigh.expression.ContextField, goal: ghidra.app.plugin.assembler.sleigh.expr.MaskedLong, vals: java.util.Map, cur: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns, hints: java.util.Set, description: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

    @overload
    def solve(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory, __a1: ghidra.app.plugin.processors.sleigh.expression.PatternExpression, __a2: ghidra.app.plugin.assembler.sleigh.expr.MaskedLong, __a3: java.util.Map, __a4: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns, __a5: java.util.Set, __a6: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

    def toString(self) -> unicode: ...

    @overload
    def valueForResolution(self, cf: ghidra.app.plugin.processors.sleigh.expression.ContextField, vals: java.util.Map, rc: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong: ...

    @overload
    def valueForResolution(self, __a0: ghidra.app.plugin.processors.sleigh.expression.PatternExpression, __a1: java.util.Map, __a2: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

