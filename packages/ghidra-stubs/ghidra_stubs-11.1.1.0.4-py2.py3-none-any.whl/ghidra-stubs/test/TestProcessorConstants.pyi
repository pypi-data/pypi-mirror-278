from typing import overload
import java.lang


class TestProcessorConstants(object):
    PROCESSOR_8051: ghidra.program.model.lang.Processor
    PROCESSOR_ARM: ghidra.program.model.lang.Processor
    PROCESSOR_DATA: ghidra.program.model.lang.Processor
    PROCESSOR_POWERPC: ghidra.program.model.lang.Processor
    PROCESSOR_SPARC: ghidra.program.model.lang.Processor
    PROCESSOR_TMS320C3x: ghidra.program.model.lang.Processor
    PROCESSOR_X86: ghidra.program.model.lang.Processor
    PROCESSOR_Z80: ghidra.program.model.lang.Processor



    def __init__(self): ...



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

