from typing import overload
import ghidra.pcode.emu.unix
import java.lang


class AbstractStreamEmuUnixFileHandle(object, ghidra.pcode.emu.unix.EmuUnixFileDescriptor):
    """
    An abstract file descriptor having no "offset," typically for stream-like files
    """

    FD_STDERR: int = 2
    FD_STDIN: int = 0
    FD_STDOUT: int = 1



    def __init__(self, machine: ghidra.pcode.emu.PcodeMachine, cSpec: ghidra.program.model.lang.CompilerSpec):
        """
        Construct a new handle
        @see AbstractEmuUnixSyscallUseropLibrary#createHandle(EmuUnixFile, int)
        @param machine the machine emulating the hardware
        @param cSpec the ABI of the target platform
        """
        ...



    def close(self) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getOffset(self) -> object: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def read(self, __a0: object) -> object: ...

    def seek(self, offset: object) -> None: ...

    def stat(self) -> ghidra.pcode.emu.unix.EmuUnixFileStat: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def write(self, __a0: object) -> object: ...

    @property
    def offset(self) -> object: ...