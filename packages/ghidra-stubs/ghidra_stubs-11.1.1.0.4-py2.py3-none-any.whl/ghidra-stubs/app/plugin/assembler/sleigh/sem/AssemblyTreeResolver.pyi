from typing import overload
import ghidra.app.plugin.assembler.sleigh.grammars
import ghidra.app.plugin.assembler.sleigh.sem
import ghidra.app.plugin.processors.sleigh
import ghidra.app.plugin.processors.sleigh.symbol
import java.lang


class AssemblyTreeResolver(ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyTreeResolver):




    def __init__(self, factory: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory, lang: ghidra.app.plugin.processors.sleigh.SleighLanguage, at: ghidra.program.model.address.Address, tree: ghidra.app.plugin.assembler.sleigh.tree.AssemblyParseBranch, context: ghidra.app.plugin.assembler.sleigh.sem.AssemblyPatternBlock, ctxGraph: ghidra.app.plugin.assembler.sleigh.sem.AssemblyContextGraph): ...



    @staticmethod
    def computeOffset(opsym: ghidra.app.plugin.processors.sleigh.symbol.OperandSymbol, cons: ghidra.app.plugin.processors.sleigh.Constructor) -> int:
        """
        Compute the offset of an operand encoded in the instruction block
 
         <p>
         TODO: Currently, there are duplicate mechanisms for resolving a constructor: 1) The newer
         mechanism implemented in {@link AssemblyConstructState}, and 2) the older one implemented in
         {@link #applyPatterns(AssemblyConstructorSemantic, int, AssemblyResolutionResults)}. The
         latter seems to require this method, since it does not have pre-computed shifts as in the
         former. We should probably remove the latter in favor of the former....
        @param opsym the operand symbol
        @param cons the constructor containing the operand
        @return the offset (right shift) to apply to the encoded operand
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getFactory(self) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyResolutionFactory: ...

    def getGrammar(self) -> ghidra.app.plugin.assembler.sleigh.grammars.AssemblyGrammar: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def resolve(self) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolutionResults:
        """
        Resolve the tree for the given parameters
        @return a set of resolutions (encodings and errors)
        """
        ...

    def resolveRootRecursion(self, temp: ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolutionResults) -> ghidra.app.plugin.assembler.sleigh.sem.AssemblyResolutionResults:
        """
        If necessary, resolve recursive constructors at the root, usually for prefixes
 
         <p>
         If there are no pure recursive constructors at the root, then this simply returns
         {@code temp} unmodified.
        @param temp the resolved root results
        @return the results with pure recursive constructors applied to obtain a compatible context
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

