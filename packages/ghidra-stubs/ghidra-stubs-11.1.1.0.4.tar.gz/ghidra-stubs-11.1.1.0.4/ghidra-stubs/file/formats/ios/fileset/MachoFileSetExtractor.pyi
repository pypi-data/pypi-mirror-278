from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.macho.commands
import ghidra.formats.gfilesystem
import ghidra.util.task
import java.lang


class MachoFileSetExtractor(object):
    FOOTER_V1: List[int]



    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def extractFileSetEntry(__a0: ghidra.app.util.bin.ByteProvider, __a1: long, __a2: ghidra.formats.gfilesystem.FSRL, __a3: ghidra.util.task.TaskMonitor) -> ghidra.app.util.bin.ByteProvider: ...

    @staticmethod
    def extractSegment(__a0: ghidra.app.util.bin.ByteProvider, __a1: ghidra.app.util.bin.format.macho.commands.SegmentCommand, __a2: ghidra.formats.gfilesystem.FSRL, __a3: ghidra.util.task.TaskMonitor) -> ghidra.app.util.bin.ByteProvider: ...

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

