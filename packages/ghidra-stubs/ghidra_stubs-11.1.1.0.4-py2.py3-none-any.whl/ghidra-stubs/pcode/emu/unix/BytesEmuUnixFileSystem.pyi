from typing import overload
import ghidra.pcode.emu.unix
import ghidra.pcode.emu.unix.BytesEmuUnixFileSystem
import java.lang
import java.util


class BytesEmuUnixFileSystem(ghidra.pcode.emu.unix.AbstractEmuUnixFileSystem):
    """
    A concrete in-memory file system simulator suitable for UNIX programs
    """





    def __init__(self):
        """
        Construct a new concrete simulated file system
        """
        ...



    def createOrGetFile(self, pathname: unicode, mode: int) -> ghidra.pcode.emu.unix.EmuUnixFile: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getFile(self, pathname: unicode) -> ghidra.pcode.emu.unix.EmuUnixFile: ...

    def hashCode(self) -> int: ...

    def newFile(self, pathname: unicode, mode: int) -> ghidra.pcode.emu.unix.BytesEmuUnixFileSystem.BytesEmuUnixFile: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def open(self, pathname: unicode, flags: java.util.Set, user: ghidra.pcode.emu.unix.EmuUnixUser, mode: int) -> ghidra.pcode.emu.unix.EmuUnixFile: ...

    def putFile(self, pathname: unicode, file: ghidra.pcode.emu.unix.EmuUnixFile) -> None: ...

    def toString(self) -> unicode: ...

    def unlink(self, pathname: unicode, user: ghidra.pcode.emu.unix.EmuUnixUser) -> None: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

