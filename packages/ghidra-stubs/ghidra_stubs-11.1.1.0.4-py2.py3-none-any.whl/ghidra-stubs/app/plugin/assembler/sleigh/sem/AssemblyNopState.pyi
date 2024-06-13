from typing import List
from typing import overload
import ghidra.app.plugin.assembler.sleigh.sem
import java.lang


class AssemblyNopState(ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyState):




    def __init__(self, __a0: ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyTreeResolver, __a1: List[object], __a2: int, __a3: ghidra.app.plugin.processors.sleigh.symbol.OperandSymbol): ...



    def computeHash(self) -> int: ...

    def equals(self, obj: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getLength(self) -> int:
        """
        Get the length in bytes of the operand represented by this node
        @return the length
        """
        ...

    def getPath(self) -> List[ghidra.app.plugin.assembler.sleigh.sem.AssemblyConstructorSemantic]: ...

    def getResolver(self) -> ghidra.app.plugin.assembler.sleigh.sem.AbstractAssemblyTreeResolver: ...

    def getShift(self) -> int: ...

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

