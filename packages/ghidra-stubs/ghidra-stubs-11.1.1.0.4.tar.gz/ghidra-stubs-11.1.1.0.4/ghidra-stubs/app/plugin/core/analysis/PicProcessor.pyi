from typing import overload
import java.lang


class PicProcessor(object):
    PROCESSOR_PIC_12: ghidra.program.model.lang.Processor
    PROCESSOR_PIC_16: ghidra.program.model.lang.Processor
    PROCESSOR_PIC_17: ghidra.program.model.lang.Processor
    PROCESSOR_PIC_18: ghidra.program.model.lang.Processor







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

