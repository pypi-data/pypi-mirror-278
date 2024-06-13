from typing import overload
import ghidra.pcode.emu.unix
import java.lang


class EmuUnixFileDescriptor(object):
    """
    A process's handle to a file (or other resource)
    """

    FD_STDERR: int = 2
    FD_STDIN: int = 0
    FD_STDOUT: int = 1







    def close(self) -> None:
        """
        Close this descriptor
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getOffset(self) -> object:
        """
        Get the current offset of the file, or 0 if not applicable
        @return the offset
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def read(self, buf: object) -> object:
        """
        Read from the file opened by this handle
        @param buf the destination buffer
        @return the number of bytes read
        @throws EmuIOException if an error occurred
        """
        ...

    def seek(self, offset: object) -> None:
        """
        See to the given offset
        @param offset the desired offset
        @throws EmuIOException if an error occurred
        """
        ...

    def stat(self) -> ghidra.pcode.emu.unix.EmuUnixFileStat:
        """
        Obtain the {@code stat} structure of the file opened by this handle
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def write(self, buf: object) -> object:
        """
        Read into the file opened by this handle
        @param buf the source buffer
        @return the number of bytes written
        @throws EmuIOException if an error occurred
        """
        ...

    @property
    def offset(self) -> object: ...