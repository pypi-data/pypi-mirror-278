from typing import List
from typing import overload
import ghidra.app.plugin.assembler.sleigh.sem
import ghidra.app.plugin.assembler.sleigh.symbol
import ghidra.app.plugin.processors.sleigh.symbol
import java.lang


class AssemblyOperandState(ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyState):
    """
    The state corresponding to a non-sub-table operand
 
 
     This is roughly analogous to ConstructState, but for assembly. However, it also records
     the value of the operand and the actual operand symbol whose value it specifies.
    """





    def __init__(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyTreeResolver, __a1: List[object], __a2: int, __a3: ghidra.app.plugin.assembler.sleigh.symbol.AssemblyTerminal, __a4: long, __a5: ghidra.app.plugin.processors.sleigh.symbol.OperandSymbol): ...



    def computeHash(self) -> int: ...

    def equals(self, obj: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getLength(self) -> int:
        """
        Get the length in bytes of the operand represented by this node
        @return the length
        """
        ...

    def getOperandSymbol(self) -> ghidra.app.plugin.processors.sleigh.symbol.OperandSymbol: ...

    def getPath(self) -> List[ghidra.app.plugin.assembler.sleigh.sem.AssemblyConstructorSemantic]: ...

    def getResolver(self) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyTreeResolver: ...

    def getShift(self) -> int: ...

    def getTerminal(self) -> ghidra.app.plugin.assembler.sleigh.symbol.AssemblyTerminal: ...

    def getValue(self) -> long: ...

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

    @property
    def operandSymbol(self) -> ghidra.app.plugin.processors.sleigh.symbol.OperandSymbol: ...

    @property
    def terminal(self) -> ghidra.app.plugin.assembler.sleigh.symbol.AssemblyTerminal: ...

    @property
    def value(self) -> long: ...