from typing import overload
import ghidra.app.plugin.assembler.sleigh.sem
import ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyStateGenerator
import java.lang
import java.util.stream


class AssemblyStringStateGenerator(ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyStateGenerator):




    def __init__(self, resolver: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyTreeResolver, node: ghidra.app.plugin.assembler.sleigh.tree.AssemblyParseToken, opSym: ghidra.app.plugin.processors.sleigh.symbol.OperandSymbol, fromLeft: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns): ...



    def equals(self, __a0: object) -> bool: ...

    def generate(self, gc: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyStateGenerator.GeneratorContext) -> java.util.stream.Stream: ...

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

