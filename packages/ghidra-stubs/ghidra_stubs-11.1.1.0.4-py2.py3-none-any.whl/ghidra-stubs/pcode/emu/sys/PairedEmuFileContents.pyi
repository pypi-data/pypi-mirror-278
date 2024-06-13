from typing import overload
import ghidra.pcode.emu.sys
import java.lang
import org.apache.commons.lang3.tuple


class PairedEmuFileContents(object, ghidra.pcode.emu.sys.EmuFileContents):
    """
    The analog of PairedPcodeExecutorStatePiece for simulated file contents
    """





    def __init__(self, left: ghidra.pcode.emu.sys.EmuFileContents, right: ghidra.pcode.emu.sys.EmuFileContents):
        """
        Create a paired file contents
        @param left the left contents
        @param right the right contents
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    def read(self, offset: long, buf: org.apache.commons.lang3.tuple.Pair, fileSize: long) -> long: ...

    @overload
    def read(self, __a0: long, __a1: object, __a2: long) -> long: ...

    def toString(self) -> unicode: ...

    def truncate(self) -> None: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @overload
    def write(self, offset: long, buf: org.apache.commons.lang3.tuple.Pair, curSize: long) -> long: ...

    @overload
    def write(self, __a0: long, __a1: object, __a2: long) -> long: ...

