from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.pe.debug
import ghidra.program.model.data
import java.lang


class DebugMisc(object, ghidra.app.util.bin.StructConverter):
    """
    A class to represent the IMAGE_DEBUG_MISC struct
     as defined in winnt.h.
 
 
 
     typedef struct _IMAGE_DEBUG_MISC {
         DWORD       DataType;               // type of misc data, see defines
         DWORD       Length;                 // total length of record, rounded to four
                                             // byte multiple.
         BOOLEAN     Unicode;                // TRUE if data is unicode string
         BYTE        Reserved[ 3 ];
         BYTE        Data[ 1 ];              // Actual data
     }
 
    """

    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    NAME: unicode = u'IMAGE_DEBUG_MISC'
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType







    def equals(self, __a0: object) -> bool: ...

    def getActualData(self) -> unicode:
        """
        Returns a string equivalent of the actual misc debug data.
        @return a string equivalent of the actual misc debug data
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getDataType(self) -> int:
        """
        Returns the data type of this misc debug.
        @return the data type of this misc debug
        """
        ...

    def getDebugDirectory(self) -> ghidra.app.util.bin.format.pe.debug.DebugDirectory:
        """
        Returns the debug directory associated with this misc debug.
        @return the debug directory associated with this misc debug
        """
        ...

    def getLength(self) -> int:
        """
        Returns the length of this misc debug.
        @return the length of this misc debug
        """
        ...

    def getReserved(self) -> List[int]:
        """
        Returns the array of reserved bytes.
        @return the array of reserved bytes
        """
        ...

    def hashCode(self) -> int: ...

    def isUnicode(self) -> bool:
        """
        Returns true if this misc debug is unicode.
        @return true if this misc debug is unicode
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType:
        """
        @see ghidra.app.util.bin.StructConverter#toDataType()
        """
        ...

    def toString(self) -> unicode:
        """
        @see java.lang.Object#toString()
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def actualData(self) -> unicode: ...

    @property
    def dataType(self) -> int: ...

    @property
    def debugDirectory(self) -> ghidra.app.util.bin.format.pe.debug.DebugDirectory: ...

    @property
    def length(self) -> int: ...

    @property
    def reserved(self) -> List[int]: ...

    @property
    def unicode(self) -> bool: ...