from typing import overload
import ghidra.app.plugin.assembler.sleigh.sem
import java.lang
import java.util.stream


class WildAssemblyStringStateGenerator(ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyStateGenerator):




    def __init__(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyTreeResolver, __a1: ghidra.asm.wild.tree.WildAssemblyParseToken, __a2: ghidra.app.plugin.processors.sleigh.symbol.OperandSymbol, __a3: unicode, __a4: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns): ...



    def equals(self, __a0: object) -> bool: ...

    def generate(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyStateGenerator.GeneratorContext) -> java.util.stream.Stream: ...

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

