from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class BTreeNodeDescriptor(object, ghidra.app.util.bin.StructConverter):
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

    def getBLink(self) -> int: ...

    def getClass(self) -> java.lang.Class: ...

    def getFLink(self) -> int: ...

    def getHeight(self) -> int: ...

    def getKind(self) -> int: ...

    def getNumRecords(self) -> int: ...

    def getRecordOffsets(self) -> List[object]: ...

    def getRecords(self) -> List[object]: ...

    def getReserved(self) -> int: ...

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
    def BLink(self) -> int: ...

    @property
    def FLink(self) -> int: ...

    @property
    def height(self) -> int: ...

    @property
    def kind(self) -> int: ...

    @property
    def numRecords(self) -> int: ...

    @property
    def recordOffsets(self) -> List[object]: ...

    @property
    def records(self) -> List[object]: ...

    @property
    def reserved(self) -> int: ...