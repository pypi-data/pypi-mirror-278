from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.dwarf
import java.lang


class StringTable(object):
    """
    Represents a DWARF string table, backed by a memory section like .debug_str.
 
     Strings are read from the section the first time requested, and then cached in a weak lookup
     table.
    """





    def __init__(self, reader: ghidra.app.util.bin.BinaryReader):
        """
        Creates a StringTable
        @param reader {@link BinaryReader} .debug_str or .debug_line_str
        """
        ...



    def clear(self) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getStringAtOffset(self, offset: long) -> unicode:
        """
        Returns the string found at <code>offset</code>, or throws an {@link IOException}
         if the offset is out of bounds.
        @param offset location of string
        @return a string, never null
        @throws IOException if not valid location
        """
        ...

    def hashCode(self) -> int: ...

    def isValid(self, offset: long) -> bool:
        """
        Returns true if the specified offset is a valid offset for this string table.
         <p>
        @param offset location of possible string
        @return boolean true if location is valid
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def of(reader: ghidra.app.util.bin.BinaryReader) -> ghidra.app.util.bin.format.dwarf.StringTable:
        """
        Creates a StringTable instance, if the supplied BinaryReader is non-null.
        @param reader BinaryReader
        @return new instance, or null if reader is null
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

