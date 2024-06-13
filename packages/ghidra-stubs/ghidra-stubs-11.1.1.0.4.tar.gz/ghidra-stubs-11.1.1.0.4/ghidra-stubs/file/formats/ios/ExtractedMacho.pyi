from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.formats.gfilesystem
import java.lang


class ExtractedMacho(object):




    def __init__(self, __a0: ghidra.app.util.bin.ByteProvider, __a1: long, __a2: ghidra.app.util.bin.format.macho.MachHeader, __a3: List[int], __a4: ghidra.util.task.TaskMonitor): ...



    def equals(self, __a0: object) -> bool: ...

    def getByteProvider(self, __a0: ghidra.formats.gfilesystem.FSRL) -> ghidra.app.util.bin.ByteProvider: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def pack(self) -> None: ...

    @staticmethod
    def toBytes(__a0: long, __a1: int) -> List[int]: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

