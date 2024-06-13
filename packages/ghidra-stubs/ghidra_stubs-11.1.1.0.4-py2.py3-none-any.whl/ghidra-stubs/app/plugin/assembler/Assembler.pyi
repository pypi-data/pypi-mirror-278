from typing import List
from typing import overload
import ghidra.app.plugin.assembler
import ghidra.app.plugin.assembler.sleigh.parse
import ghidra.app.plugin.assembler.sleigh.sem
import ghidra.program.model.address
import ghidra.program.model.lang
import ghidra.program.model.listing
import java.lang
import java.util


class Assembler(ghidra.app.plugin.assembler.GenericAssembler, object):
    """
    The primary interface for performing assembly in Ghidra.
 
 
     Use the Assemblers class to obtain a suitable implementation for a given program or
     language.
    """









    def assemble(self, __a0: ghidra.program.model.address.Address, __a1: List[unicode]) -> ghidra.program.model.listing.InstructionIterator: ...

    @overload
    def assembleLine(self, __a0: ghidra.program.model.address.Address, __a1: unicode) -> List[int]: ...

    @overload
    def assembleLine(self, __a0: ghidra.program.model.address.Address, __a1: unicode, __a2: ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock) -> List[int]: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getContextAt(self, __a0: ghidra.program.model.address.Address) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock: ...

    def getLanguage(self) -> ghidra.program.model.lang.Language: ...

    def getProgram(self) -> ghidra.program.model.listing.Program: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parseLine(self, __a0: unicode) -> java.util.Collection: ...

    @overload
    def patchProgram(self, __a0: List[int], __a1: ghidra.program.model.address.Address) -> ghidra.program.model.listing.InstructionIterator: ...

    @overload
    def patchProgram(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolvedPatterns, __a1: ghidra.program.model.address.Address) -> ghidra.program.model.listing.Instruction: ...

    @overload
    def resolveLine(self, __a0: ghidra.program.model.address.Address, __a1: unicode) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolutionResults: ...

    @overload
    def resolveLine(self, __a0: ghidra.program.model.address.Address, __a1: unicode, __a2: ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolutionResults: ...

    @overload
    def resolveTree(self, __a0: ghidra.app.plugin.assembler.sleigh.parse.AssemblyParseResult, __a1: ghidra.program.model.address.Address) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolutionResults: ...

    @overload
    def resolveTree(self, __a0: ghidra.app.plugin.assembler.sleigh.parse.AssemblyParseResult, __a1: ghidra.program.model.address.Address, __a2: ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolutionResults: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def language(self) -> ghidra.program.model.lang.Language: ...

    @property
    def program(self) -> ghidra.program.model.listing.Program: ...