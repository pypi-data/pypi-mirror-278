from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.macos.rm
import ghidra.program.model.data
import java.lang


class ResourceMap(object, ghidra.app.util.bin.StructConverter):
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

    def getClass(self) -> java.lang.Class: ...

    def getCopy(self) -> ghidra.app.util.bin.format.macos.rm.ResourceHeader: ...

    def getFileReferenceNumber(self) -> int: ...

    def getHandleToNextResourceMap(self) -> int: ...

    def getMapStartIndex(self) -> long: ...

    def getNumberOfTypes(self) -> int: ...

    def getReferenceEntryList(self) -> List[ghidra.app.util.bin.format.macos.rm.ReferenceListEntry]: ...

    def getResourceForkAttributes(self) -> int: ...

    def getResourceNameListOffset(self) -> int: ...

    def getResourceTypeList(self) -> List[ghidra.app.util.bin.format.macos.rm.ResourceType]: ...

    def getResourceTypeListOffset(self) -> int: ...

    def getStringAt(self, offset: int) -> unicode: ...

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
    def copy(self) -> ghidra.app.util.bin.format.macos.rm.ResourceHeader: ...

    @property
    def fileReferenceNumber(self) -> int: ...

    @property
    def handleToNextResourceMap(self) -> int: ...

    @property
    def mapStartIndex(self) -> long: ...

    @property
    def numberOfTypes(self) -> int: ...

    @property
    def referenceEntryList(self) -> List[object]: ...

    @property
    def resourceForkAttributes(self) -> int: ...

    @property
    def resourceNameListOffset(self) -> int: ...

    @property
    def resourceTypeList(self) -> List[object]: ...

    @property
    def resourceTypeListOffset(self) -> int: ...