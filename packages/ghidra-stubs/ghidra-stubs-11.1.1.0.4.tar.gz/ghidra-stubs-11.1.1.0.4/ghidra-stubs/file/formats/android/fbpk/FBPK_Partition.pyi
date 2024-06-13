from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.importer
import ghidra.program.model.address
import ghidra.program.model.data
import ghidra.program.model.listing
import ghidra.util.task
import java.lang


class FBPK_Partition(object, ghidra.app.util.bin.StructConverter):
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



    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDataSize(self) -> int: ...

    def getDataStartOffset(self) -> long: ...

    def getHeaderSize(self) -> int: ...

    def getName(self) -> unicode: ...

    def getOffsetToNextPartitionTable(self) -> int: ...

    def getPartitionIndex(self) -> int: ...

    def getType(self) -> int: ...

    def hashCode(self) -> int: ...

    def isFile(self) -> bool: ...

    def markup(self, __a0: ghidra.program.model.listing.Program, __a1: ghidra.program.model.address.Address, __a2: ghidra.util.task.TaskMonitor, __a3: ghidra.app.util.importer.MessageLog) -> None: ...

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
    def dataSize(self) -> int: ...

    @property
    def dataStartOffset(self) -> long: ...

    @property
    def file(self) -> bool: ...

    @property
    def headerSize(self) -> int: ...

    @property
    def name(self) -> unicode: ...

    @property
    def offsetToNextPartitionTable(self) -> int: ...

    @property
    def partitionIndex(self) -> int: ...

    @property
    def type(self) -> int: ...