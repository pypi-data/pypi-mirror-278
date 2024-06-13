from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class ResourceDirectoryString(object, ghidra.app.util.bin.StructConverter):
    """

     typedef struct _IMAGE_RESOURCE_DIRECTORY_STRING {
         WORD    Length;
         CHAR    NameString[ 1 ];
     };
 
    """

    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    NAME: unicode = u'IMAGE_RESOURCE_DIRECTORY_STRING'
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader, index: int):
        """
        Constructor.
        @param reader the binary reader
        @param index the index where this resource string begins
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getLength(self) -> int:
        """
        Returns the length of the string, in bytes.
        @return the length of the string, in bytes
        """
        ...

    def getNameString(self) -> unicode:
        """
        Returns the resource name string.
        @return the resource name string
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def length(self) -> int: ...

    @property
    def nameString(self) -> unicode: ...