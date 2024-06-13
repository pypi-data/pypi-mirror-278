from typing import List
from typing import overload
import ghidra.pcode.emu.sys
import java.lang


class BytesEmuFileContents(object, ghidra.pcode.emu.sys.EmuFileContents):
    """
    A concrete in-memory bytes store for simulated file contents
 
 
     Note that currently, the total contents cannot exceed a Java array, so the file must remain less
     than 2GB in size.
    """





    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    def read(self, offset: long, buf: List[int], fileSize: long) -> long: ...

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
    def write(self, offset: long, buf: List[int], curSize: long) -> long: ...

    @overload
    def write(self, __a0: long, __a1: object, __a2: long) -> long: ...

