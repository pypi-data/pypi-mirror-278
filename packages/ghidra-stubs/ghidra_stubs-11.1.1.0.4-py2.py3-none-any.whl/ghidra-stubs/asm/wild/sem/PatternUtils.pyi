from typing import overload
import ghidra.app.plugin.assembler.sleigh.sem
import ghidra.app.plugin.processors.sleigh.expression
import ghidra.asm.wild.sem
import java.lang


class PatternUtils(object):








    @staticmethod
    def castWild(__a0: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns) -> ghidra.asm.wild.sem.WildAssemblyResolvedPatterns: ...

    @staticmethod
    def collectLocation(__a0: ghidra.app.plugin.processors.sleigh.expression.PatternExpression) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock: ...

    def equals(self, __a0: object) -> bool: ...

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

