from typing import overload
import ghidra.app.plugin.assembler.sleigh.sem
import java.lang
import java.util.stream


class WildAssemblyConstructStateGenerator(ghidra.app.plugin.assembler.sleigh.sem.AssemblyHiddenConstructStateGenerator):




    def __init__(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyTreeResolver, __a1: ghidra.app.plugin.processors.sleigh.symbol.SubtableSymbol, __a2: unicode, __a3: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns): ...



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

