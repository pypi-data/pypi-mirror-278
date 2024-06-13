from typing import overload
import ghidra.pcode.emu.unix
import java.lang


class DefaultEmuUnixFileHandle(object, ghidra.pcode.emu.unix.EmuUnixFileDescriptor):
    """
    A file descriptor associated with a file on a simulated UNIX file system
    """

    FD_STDERR: int = 2
    FD_STDIN: int = 0
    FD_STDOUT: int = 1



    def __init__(self, machine: ghidra.pcode.emu.PcodeMachine, cSpec: ghidra.program.model.lang.CompilerSpec, file: ghidra.pcode.emu.unix.EmuUnixFile, flags: java.util.Set, user: ghidra.pcode.emu.unix.EmuUnixUser):
        """
        Construct a new handle on the given file
        @see AbstractEmuUnixSyscallUseropLibrary#createHandle(EmuUnixFile, int)
        @param machine the machine emulating the hardware
        @param cSpec the ABI of the target platform
        @param file the file opened by this handle
        @param flags the user-specified flags, as defined by the simulator
        @param user the user that opened the file
        """
        ...



    def checkReadable(self) -> None:
        """
        Check if the file is readable, throwing {@link EmuIOException} if not
        """
        ...

    def checkWritable(self) -> None:
        """
        Check if the file is writable, throwing {@link EmuIOException} if not
        """
        ...

    def close(self) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getFile(self) -> ghidra.pcode.emu.unix.EmuUnixFile:
        """
        Get the file opened to this handle
        @return the file
        """
        ...

    def getOffset(self) -> object: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def read(self, buf: object) -> object: ...

    def seek(self, offset: object) -> None: ...

    def stat(self) -> ghidra.pcode.emu.unix.EmuUnixFileStat: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def write(self, buf: object) -> object: ...

    @property
    def file(self) -> ghidra.pcode.emu.unix.EmuUnixFile: ...

    @property
    def offset(self) -> object: ...