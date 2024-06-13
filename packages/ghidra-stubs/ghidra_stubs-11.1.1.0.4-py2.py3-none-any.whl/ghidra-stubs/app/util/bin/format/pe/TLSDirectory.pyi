from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class TLSDirectory(object, ghidra.app.util.bin.StructConverter):
    """
    A class to represent the IMAGE_TLS_DIRECTORY32 and
     IMAGE_TLS_DIRECTORY64 data structures.
 
 
     typedef struct _IMAGE_TLS_DIRECTORY32 {
         DWORD   StartAddressOfRawData;
         DWORD   EndAddressOfRawData;
         DWORD   AddressOfIndex;             // PDWORD
         DWORD   AddressOfCallBacks;         // PIMAGE_TLS_CALLBACK *
         DWORD   SizeOfZeroFill;
         DWORD   Characteristics;
     } IMAGE_TLS_DIRECTORY32;
     typedef IMAGE_TLS_DIRECTORY32 * PIMAGE_TLS_DIRECTORY32;
 
 
 
     typedef struct _IMAGE_TLS_DIRECTORY64 {
         ULONGLONG   StartAddressOfRawData;
         ULONGLONG   EndAddressOfRawData;
         PDWORD      AddressOfIndex;
         PIMAGE_TLS_CALLBACK * AddressOfCallBacks;
         DWORD       SizeOfZeroFill;
         DWORD       Characteristics;
     } IMAGE_TLS_DIRECTORY64;
     typedef IMAGE_TLS_DIRECTORY64 * PIMAGE_TLS_DIRECTORY64;
 
 
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







    def equals(self, __a0: object) -> bool: ...

    def getAddressOfCallBacks(self) -> long:
        """
        @return the address of an array of <code>PIMAGE_TLS_CALLBACK</code> function pointers
        """
        ...

    def getAddressOfIndex(self) -> long:
        """
        @return the index to locate the thread local data.
        """
        ...

    def getCharacteristics(self) -> int:
        """
        Reserved, currently set to 0.
        @return reserved, currently set to 0
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getEndAddressOfRawData(self) -> long:
        """
        Returns the ending address of the range of memory used to initialize a new thread's TLS data in memory.
        @return the ending address of the range of memory used to initialize a new thread's TLS data in memory.
        """
        ...

    def getName(self) -> unicode:
        """
        Returns the name of the structure.
        @return the name of the structure
        """
        ...

    def getSizeOfZeroFill(self) -> int:
        """
        @return the size in bytes of the initialization data
        """
        ...

    def getStartAddressOfRawData(self) -> long:
        """
        Returns the beginning address of a range of memory used to initialize a new thread's TLS data in memory.
        @return the beginning address of a range of memory used to initialize a new thread's TLS data in memory.
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

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
    def addressOfCallBacks(self) -> long: ...

    @property
    def addressOfIndex(self) -> long: ...

    @property
    def characteristics(self) -> int: ...

    @property
    def endAddressOfRawData(self) -> long: ...

    @property
    def name(self) -> unicode: ...

    @property
    def sizeOfZeroFill(self) -> int: ...

    @property
    def startAddressOfRawData(self) -> long: ...