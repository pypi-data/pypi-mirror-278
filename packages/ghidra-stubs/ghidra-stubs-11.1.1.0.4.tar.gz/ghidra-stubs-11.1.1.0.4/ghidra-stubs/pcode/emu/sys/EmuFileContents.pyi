from typing import overload
import java.lang


class EmuFileContents(object):
    """
    The content store to back a simulated file

 
     TODO: Could/should this just be the same interface as an execute state? If so, we'd need to
     formalize the store interface and require one for each address space in the state. Sharing that
     interface may not be a good idea.... I think implementors can use a common realization if that
     suits them.
 
 
     TODO: Actually, a better idea might be to introduce an address factory with custom spaces into
     the emulator. Then a library/file could just create an address space and use the state to store
     and retrieve the file contents. Better yet, when written down, those contents and markings could
     appear in the user's trace.
    """









    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def read(self, offset: long, buf: object, fileSize: long) -> long:
        """
        Copy values from the file into the given buffer
        @param offset the offset in the file to read
        @param buf the destination buffer, whose size must be known
        @param fileSize the size of the file
        @return the number of bytes (not necessarily concrete) read
        """
        ...

    def toString(self) -> unicode: ...

    def truncate(self) -> None:
        """
        Erase the contents
 
         <p>
         Note that the file's size will be set to 0, so actual erasure of the contents may not be
         necessary, but if the contents are expensive to store, they ought to be disposed.
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def write(self, offset: long, buf: object, curSize: long) -> long:
        """
        Write values from the given buffer into the file
        @param offset the offset in the file to write
        @param buf the source buffer, whose size must be known
        @param curSize the current size of the file
        @return the number of bytes (not necessarily concrete) written
        """
        ...

