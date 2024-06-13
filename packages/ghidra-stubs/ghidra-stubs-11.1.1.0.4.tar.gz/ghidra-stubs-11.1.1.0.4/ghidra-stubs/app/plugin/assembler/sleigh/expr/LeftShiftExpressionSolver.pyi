from typing import overload
import ghidra.app.plugin.assembler.sleigh.expr
import ghidra.app.plugin.assembler.sleigh.sem
import ghidra.app.plugin.processors.sleigh.expression
import java.lang
import java.util


class LeftShiftExpressionSolver(ghidra.app.plugin.assembler.sleigh.expr.AbstractBinaryExpressionSolver):
    """
    Solves expressions of the form 
    """





    def __init__(self): ...



    def compute(self, lval: ghidra.app.plugin.assembler.sleigh.expr.MaskedLong, rval: ghidra.app.plugin.assembler.sleigh.expr.MaskedLong) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong: ...

    def computeLeft(self, rval: ghidra.app.plugin.assembler.sleigh.expr.MaskedLong, goal: ghidra.app.plugin.assembler.sleigh.expr.MaskedLong) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong: ...

    def computeRight(self, lval: ghidra.app.plugin.assembler.sleigh.expr.MaskedLong, goal: ghidra.app.plugin.assembler.sleigh.expr.MaskedLong) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @overload
    def getInstructionLength(self, __a0: ghidra.app.plugin.processors.sleigh.expression.BinaryExpression) -> int: ...

    @overload
    def getInstructionLength(self, __a0: ghidra.app.plugin.processors.sleigh.expression.PatternExpression) -> int: ...

    @overload
    def getValue(self, __a0: ghidra.app.plugin.processors.sleigh.expression.BinaryExpression, __a1: java.util.Map, __a2: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong: ...

    @overload
    def getValue(self, __a0: ghidra.app.plugin.processors.sleigh.expression.PatternExpression, __a1: java.util.Map, __a2: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    def solve(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory, __a1: ghidra.app.plugin.processors.sleigh.expression.BinaryExpression, __a2: ghidra.app.plugin.assembler.sleigh.expr.MaskedLong, __a3: java.util.Map, __a4: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns, __a5: java.util.Set, __a6: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

    @overload
    def solve(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory, __a1: ghidra.app.plugin.processors.sleigh.expression.PatternExpression, __a2: ghidra.app.plugin.assembler.sleigh.expr.MaskedLong, __a3: java.util.Map, __a4: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns, __a5: java.util.Set, __a6: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolution: ...

    def toString(self) -> unicode: ...

    @overload
    def valueForResolution(self, __a0: ghidra.app.plugin.processors.sleigh.expression.BinaryExpression, __a1: java.util.Map, __a2: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong: ...

    @overload
    def valueForResolution(self, __a0: ghidra.app.plugin.processors.sleigh.expression.PatternExpression, __a1: java.util.Map, __a2: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns) -> ghidra.app.plugin.assembler.sleigh.expr.MaskedLong: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

