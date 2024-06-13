from typing import overload
import ghidra.app.plugin.assembler
import ghidra.app.plugin.assembler.sleigh
import ghidra.program.model.lang
import ghidra.program.model.listing
import java.lang


class WildSleighAssemblerBuilder(ghidra.app.plugin.assembler.sleigh.AbstractSleighAssemblerBuilder):




    def __init__(self, __a0: ghidra.app.plugin.processors.sleigh.SleighLanguage): ...



    def equals(self, __a0: object) -> bool: ...

    @overload
    def getAssembler(self, __a0: ghidra.app.plugin.assembler.AssemblySelector) -> ghidra.app.plugin.assembler.GenericAssembler: ...

    @overload
    def getAssembler(self, __a0: ghidra.app.plugin.assembler.AssemblySelector, __a1: ghidra.program.model.listing.Program) -> ghidra.app.plugin.assembler.GenericAssembler: ...

    def getClass(self) -> java.lang.Class: ...

    def getLanguage(self) -> ghidra.program.model.lang.Language: ...

    def getLanguageID(self) -> ghidra.program.model.lang.LanguageID: ...

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

