from typing import overload
import ghidra.pcode.emu.unix
import ghidra.pcode.exec
import java.lang


class EmuUnixFile(object):
    """
    A simulated UNIX file

 
     Contrast this with EmuUnixFileDescriptor, which is a process's handle to an open file,
     not the file itself.
    """









    def checkReadable(self, user: ghidra.pcode.emu.unix.EmuUnixUser) -> None:
        """
        Require the user to have read permission on this file, throwing {@link EmuIOException} if not
        @param user the user
        """
        ...

    def checkWritable(self, user: ghidra.pcode.emu.unix.EmuUnixUser) -> None:
        """
        Require the user to have write permission on this file, throwing {@link EmuIOException} if
         not
        @param user the user
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getPathname(self) -> unicode:
        """
        Get the original pathname of this file
 
         <p>
         Depending on the fidelity of the file system simulator, and the actions taken by the target
         program, the file may no longer actually exist at this path, but it ought be have been the
         pathname at some point in the file life.
        @return the pathname
        """
        ...

    def getStat(self) -> ghidra.pcode.emu.unix.EmuUnixFileStat:
        """
        Get the file's {@code stat} structure, as defined by the simulator.
        @return the stat
        """
        ...

    def hashCode(self) -> int: ...

    def isReadable(self, user: ghidra.pcode.emu.unix.EmuUnixUser) -> bool:
        """
        Check if the given user can read this file
        @param user the user
        @return true if permitted, false otherwise
        """
        ...

    def isWritable(self, user: ghidra.pcode.emu.unix.EmuUnixUser) -> bool:
        """
        Check if the given user can write this file
        @param user the user
        @return true if permitted, false otherwise
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def read(self, arithmetic: ghidra.pcode.exec.PcodeArithmetic, offset: object, buf: object) -> object:
        """
        Read contents from the file starting at the given offset into the given buffer
 
         <p>
         This roughly follows the semantics of the UNIX {@code read()}. While the offset and return
         value may depend on the arithmetic, the actual contents read from the file should not.
        @param arithmetic the arithmetic
        @param offset the offset
        @param buf the buffer
        @return the number of bytes read
        """
        ...

    def toString(self) -> unicode: ...

    def truncate(self) -> None:
        """
        Erase the contents of the file
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def write(self, arithmetic: ghidra.pcode.exec.PcodeArithmetic, offset: object, buf: object) -> object:
        """
        Write contents into the file starting at the given offset from the given buffer
 
         <p>
         This roughly follows the semantics of the UNIX {@code write()}. While the offset and return
         value may depend on the arithmetic, the actual contents written to the file should not.
        @param arithmetic the arithmetic
        @param offset the offset
        @param buf the buffer
        @return the number of bytes written
        """
        ...

    @property
    def pathname(self) -> unicode: ...

    @property
    def stat(self) -> ghidra.pcode.emu.unix.EmuUnixFileStat: ...