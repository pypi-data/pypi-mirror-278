from typing import List
from typing import overload
import ghidra.pcode.emu.unix
import java.lang
import java.util


class EmuUnixFileSystem(object):
    """
    A simulated UNIX file system
    """






    class OpenFlag(java.lang.Enum):
        O_APPEND: ghidra.pcode.emu.unix.EmuUnixFileSystem.OpenFlag
        O_CREAT: ghidra.pcode.emu.unix.EmuUnixFileSystem.OpenFlag
        O_RDONLY: ghidra.pcode.emu.unix.EmuUnixFileSystem.OpenFlag
        O_RDWR: ghidra.pcode.emu.unix.EmuUnixFileSystem.OpenFlag
        O_TRUNC: ghidra.pcode.emu.unix.EmuUnixFileSystem.OpenFlag
        O_WRONLY: ghidra.pcode.emu.unix.EmuUnixFileSystem.OpenFlag







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDeclaringClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        @staticmethod
        def isRead(__a0: java.util.Collection) -> bool: ...

        @staticmethod
        def isWrite(__a0: java.util.Collection) -> bool: ...

        def name(self) -> unicode: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def ordinal(self) -> int: ...

        @overload
        @staticmethod
        def set(__a0: List[ghidra.pcode.emu.unix.EmuUnixFileSystem.OpenFlag]) -> java.util.Set: ...

        @overload
        @staticmethod
        def set(__a0: java.util.Collection) -> java.util.Set: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.pcode.emu.unix.EmuUnixFileSystem.OpenFlag: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.pcode.emu.unix.EmuUnixFileSystem.OpenFlag]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...







    def createOrGetFile(self, pathname: unicode, mode: int) -> ghidra.pcode.emu.unix.EmuUnixFile:
        """
        Get the named file, creating it if it doesn't already exist
 
         <p>
         This is accessed by the emulator user, not the target program.
        @param pathname the pathname of the requested file
        @param mode the mode of a created file. Ignored if the file exists
        @return the file
        @throws EmuIOException if an error occurred
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getFile(self, pathname: unicode) -> ghidra.pcode.emu.unix.EmuUnixFile:
        """
        Get the named file
 
         <p>
         This is accessed by the emulator user, not the target program.
        @param pathname the pathname of the requested file
        @return the file, or {@code null} if it doesn't exist
        @throws EmuIOException if an error occurred
        """
        ...

    def hashCode(self) -> int: ...

    def newFile(self, pathname: unicode, mode: int) -> ghidra.pcode.emu.unix.EmuUnixFile:
        """
        A factory for constructing a new file (without adding it to the file system)
        @param pathname the path of the file
        @param mode the mode of the new file
        @return the new file
        @throws EmuIOException if the file cannot be constructed
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def open(self, pathname: unicode, flags: java.util.Set, user: ghidra.pcode.emu.unix.EmuUnixUser, mode: int) -> ghidra.pcode.emu.unix.EmuUnixFile:
        """
        Open the requested file according to the given flags and user
 
         <p>
         This is generally accessed by the target program via a {@link DefaultEmuUnixFileHandle}.
        @param pathname the pathname of the requested file
        @param flags the requested open flags
        @param user the user making the request
        @param mode the mode to assign the file, if created. Otherwise ignored
        @return the file
        @throws EmuIOException if an error occurred, e.g., file not found, or access denied
        """
        ...

    def putFile(self, pathname: unicode, file: ghidra.pcode.emu.unix.EmuUnixFile) -> None:
        """
        Place the given file at the given location
 
         <p>
         This is accessed by the emulator user, not the target program. If the file already exists, it
         is replaced silently.
        @param pathname the pathname of the file
        @param file the file, presumably having the same pathname
        @throws EmuIOException if an error occurred
        """
        ...

    def toString(self) -> unicode: ...

    def unlink(self, pathname: unicode, user: ghidra.pcode.emu.unix.EmuUnixUser) -> None:
        """
        Remove the file at the given location
 
         <p>
         TODO: Separate the user-facing routine from the target-facing routine.
 
         <p>
         If the file does not exist, this has no effect.
        @param pathname the pathname of the file to unlink
        @param user the user requesting the unlink
        @throws EmuIOException if an error occurred
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

