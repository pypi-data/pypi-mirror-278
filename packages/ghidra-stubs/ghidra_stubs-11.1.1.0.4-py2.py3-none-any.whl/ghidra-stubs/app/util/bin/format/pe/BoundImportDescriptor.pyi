from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.pe
import ghidra.program.model.data
import ghidra.util
import java.lang


class BoundImportDescriptor(object, ghidra.app.util.bin.StructConverter, ghidra.app.util.bin.ByteArrayConverter):
    """
    A class to represent the 
     IMAGE_BOUND_IMPORT_DESCRIPTOR
     data structure defined in winnt.h.
 
 
     typedef struct _IMAGE_BOUND_IMPORT_DESCRIPTOR {
         DWORD   TimeDateStamp;
         WORD    OffsetModuleName;
         WORD    NumberOfModuleForwarderRefs;
         // Array of zero or more IMAGE_BOUND_FORWARDER_REF follows
     } IMAGE_BOUND_IMPORT_DESCRIPTOR,  *PIMAGE_BOUND_IMPORT_DESCRIPTOR;
 
    """

    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    IMAGE_SIZEOF_BOUND_IMPORT_DESCRIPTOR: int = 8
    NAME: unicode = u'IMAGE_BOUND_IMPORT_DESCRIPTOR'
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType



    def __init__(self, name: unicode, timeDateStamp: int): ...



    def equals(self, __a0: object) -> bool: ...

    def getBoundImportForwarderRef(self, index: int) -> ghidra.app.util.bin.format.pe.BoundImportForwarderRef:
        """
        Returns the forwarder ref at the specified index
        @param index the index of the forwarder ref
        @return the forwarder ref at the specified index
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getModuleName(self) -> unicode:
        """
        Returns the module name of the imported DLL.
        @return the module name of the imported DLL
        """
        ...

    def getNumberOfModuleForwarderRefs(self) -> int:
        """
        Returns the number of IMAGE_BOUND_FORWARDER_REF 
         structures that immediately follow this structure.
        @return the number of IMAGE_BOUND_FORWARDER_REF structures that immediately follow this structure
        """
        ...

    def getOffsetModuleName(self) -> int:
        """
        Returns an offset to a string with the name of the imported DLL.
        @return an offset to a string with the name
        """
        ...

    def getTimeDateStamp(self) -> int:
        """
        Returns the time/data stamp of the imported DLL.
        @return the time/data stamp of the imported DLL
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

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
    def moduleName(self) -> unicode: ...

    @property
    def numberOfModuleForwarderRefs(self) -> int: ...

    @property
    def offsetModuleName(self) -> int: ...

    @property
    def timeDateStamp(self) -> int: ...