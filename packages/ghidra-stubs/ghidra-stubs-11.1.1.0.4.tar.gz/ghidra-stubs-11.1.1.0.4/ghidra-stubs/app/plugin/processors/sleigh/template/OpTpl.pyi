from typing import List
from typing import overload
import ghidra.app.plugin.processors.sleigh.template
import ghidra.program.model.pcode
import java.lang


class OpTpl(object):
    """
    Placeholder for what will resolve to a PcodeOp
     for a specific InstructionContext
    """





    def __init__(self, opcode: int, output: ghidra.app.plugin.processors.sleigh.template.VarnodeTpl, inputs: List[ghidra.app.plugin.processors.sleigh.template.VarnodeTpl]): ...



    def decode(self, decoder: ghidra.program.model.pcode.Decoder) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getInput(self) -> List[ghidra.app.plugin.processors.sleigh.template.VarnodeTpl]: ...

    def getOpcode(self) -> int: ...

    def getOutput(self) -> ghidra.app.plugin.processors.sleigh.template.VarnodeTpl: ...

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
    def input(self) -> List[ghidra.app.plugin.processors.sleigh.template.VarnodeTpl]: ...

    @property
    def opcode(self) -> int: ...

    @property
    def output(self) -> ghidra.app.plugin.processors.sleigh.template.VarnodeTpl: ...