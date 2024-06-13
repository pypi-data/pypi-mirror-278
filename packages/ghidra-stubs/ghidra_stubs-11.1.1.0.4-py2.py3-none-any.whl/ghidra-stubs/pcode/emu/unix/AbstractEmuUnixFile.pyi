from typing import overload
import ghidra.pcode.emu.unix
import ghidra.pcode.exec
import java.lang


class AbstractEmuUnixFile(object, ghidra.pcode.emu.unix.EmuUnixFile):
    """
    An abstract file contained in an emulated file system

 
     Contrast this with DefaultEmuUnixFileHandle, which is a particular process's handle when
     opening the file, not the file itself.
    """





    def __init__(self, pathname: unicode, mode: int):
        """
        Construct a new file
 
         <p>
         TODO: Technically, a file can be hardlinked to several pathnames, but for simplicity, or for
         diagnostics, we let the file know its own original name.
        @see AbstractEmuUnixFileSystem#newFile(String, int)
        @param pathname the pathname of the file
        @param mode the mode of the file
        """
        ...



    def checkReadable(self, __a0: ghidra.pcode.emu.unix.EmuUnixUser) -> None: ...

    def checkWritable(self, __a0: ghidra.pcode.emu.unix.EmuUnixUser) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getPathname(self) -> unicode: ...

    def getStat(self) -> ghidra.pcode.emu.unix.EmuUnixFileStat: ...

    def hashCode(self) -> int: ...

    def isReadable(self, __a0: ghidra.pcode.emu.unix.EmuUnixUser) -> bool: ...

    def isWritable(self, __a0: ghidra.pcode.emu.unix.EmuUnixUser) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def read(self, arithmetic: ghidra.pcode.exec.PcodeArithmetic, offset: object, buf: object) -> object: ...

    def toString(self) -> unicode: ...

    def truncate(self) -> None: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def write(self, arithmetic: ghidra.pcode.exec.PcodeArithmetic, offset: object, buf: object) -> object: ...

    @property
    def pathname(self) -> unicode: ...

    @property
    def stat(self) -> ghidra.pcode.emu.unix.EmuUnixFileStat: ...