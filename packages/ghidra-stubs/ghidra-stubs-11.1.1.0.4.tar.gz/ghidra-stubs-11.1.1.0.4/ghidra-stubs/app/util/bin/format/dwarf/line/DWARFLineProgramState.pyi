from typing import overload
import ghidra.app.util.bin.format.dwarf.line
import java.lang


class DWARFLineProgramState(object):
    address: long
    column: int
    discriminator: long
    epilogueBegin: bool
    file: int
    isBasicBlock: bool
    isEndSequence: bool
    isStatement: bool
    isa: long
    line: int
    prologueEnd: bool



    @overload
    def __init__(self, defaultIsStatement: bool): ...

    @overload
    def __init__(self, other: ghidra.app.util.bin.format.dwarf.line.DWARFLineProgramState): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def isSameFileLine(self, other: ghidra.app.util.bin.format.dwarf.line.DWARFLineProgramState) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

