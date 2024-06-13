from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.pe
import ghidra.program.model.data
import ghidra.util
import java.lang


class ThunkData(object, ghidra.app.util.bin.StructConverter, ghidra.app.util.bin.ByteArrayConverter):
    """
    A class to represent the 
     IMAGE_THUNK_DATA32 struct
     as defined in 
     winnt.h.
 
 
     typedef struct _IMAGE_THUNK_DATA32 {
         union {
             DWORD ForwarderString;  // PBYTE
             DWORD Function;         // PDWORD
             DWORD Ordinal;
             DWORD AddressOfData;    // PIMAGE_IMPORT_BY_NAME
         } u1;
     } IMAGE_THUNK_DATA32;
     typedef IMAGE_THUNK_DATA32 * PIMAGE_THUNK_DATA32;
 
 
 
     typedef struct _IMAGE_THUNK_DATA64 {
         union {
             PBYTE  ForwarderString;
             PDWORD Function;
             ULONGLONG Ordinal;
             PIMAGE_IMPORT_BY_NAME  AddressOfData;
         } u1;
     } IMAGE_THUNK_DATA64;
     typedef IMAGE_THUNK_DATA64 * PIMAGE_THUNK_DATA64;
 
    """

    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType



    def __init__(self, value: int):
        """
        Constructs a new thunk data with the specified value
        @param value the new thunk value
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getAddressOfData(self) -> long:
        """
        Returns the address of the data.
        @return the address of the data
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getForwarderString(self) -> long:
        """
        Returns the forward string pointer.
        @return the forward string pointer
        """
        ...

    def getFunction(self) -> long:
        """
        Returns the function pointer.
        @return the function pointer
        """
        ...

    def getImportByName(self) -> ghidra.app.util.bin.format.pe.ImportByName:
        """
        Returns the underlying import by name structure.
        @return the underlying import by name structure
        """
        ...

    def getOrdinal(self) -> long:
        """
        Returns the ordinal.
        @return the ordinal
        """
        ...

    def getStructName(self) -> unicode:
        """
        Returns the struct name.
        @return the struct name
        """
        ...

    def getStructSize(self) -> int:
        """
        Returns the size of the thunk (in bytes) based on the size of the
         executable (32 vs 64 bit).
        @return the size of the thunk (in bytes)
        """
        ...

    def hashCode(self) -> int: ...

    def isOrdinal(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setValue(self, value: int) -> None:
        """
        Sets the value of the thunk.
        @param value the new thunk value
        """
        ...

    def toBytes(self, dc: ghidra.util.DataConverter) -> List[int]:
        """
        @see ghidra.app.util.bin.ByteArrayConverter#toBytes(ghidra.util.DataConverter)
        """
        ...

    def toDataType(self) -> ghidra.program.model.data.DataType:
        """
        @see ghidra.app.util.bin.StructConverter#toDataType()
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def addressOfData(self) -> long: ...

    @property
    def forwarderString(self) -> long: ...

    @property
    def function(self) -> long: ...

    @property
    def importByName(self) -> ghidra.app.util.bin.format.pe.ImportByName: ...

    @property
    def ordinal(self) -> bool: ...

    @property
    def structName(self) -> unicode: ...

    @property
    def structSize(self) -> int: ...

    @property
    def value(self) -> None: ...  # No getter available.

    @value.setter
    def value(self, value: int) -> None: ...