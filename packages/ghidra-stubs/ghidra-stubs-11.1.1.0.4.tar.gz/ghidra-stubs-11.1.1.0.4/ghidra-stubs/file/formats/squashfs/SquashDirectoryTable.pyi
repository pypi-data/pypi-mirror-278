from typing import List
from typing import overload
import ghidra.file.formats.squashfs
import ghidra.util.task
import java.lang


class SquashDirectoryTable(object):




    def __init__(self, __a0: ghidra.app.util.bin.BinaryReader, __a1: ghidra.file.formats.squashfs.SquashSuperBlock, __a2: ghidra.file.formats.squashfs.SquashFragmentTable, __a3: ghidra.util.task.TaskMonitor): ...



    def assignInodes(self, __a0: ghidra.file.formats.squashfs.SquashInodeTable, __a1: ghidra.util.task.TaskMonitor) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getHeaders(self, __a0: ghidra.file.formats.squashfs.SquashBasicDirectoryInode) -> List[object]: ...

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

