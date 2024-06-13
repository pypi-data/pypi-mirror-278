from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class PefDebug(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SIZEOF: int = 18
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType



    def __init__(self, memory: ghidra.program.model.mem.Memory, address: ghidra.program.model.address.Address): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDistance(self) -> int: ...

    def getFlags(self) -> int: ...

    def getName(self) -> unicode: ...

    def getNameLength(self) -> int: ...

    def getType(self) -> int: ...

    def getUnknown(self) -> int: ...

    def hashCode(self) -> int: ...

    def isValid(self) -> bool: ...

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
    def distance(self) -> int: ...

    @property
    def flags(self) -> int: ...

    @property
    def name(self) -> unicode: ...

    @property
    def nameLength(self) -> int: ...

    @property
    def type(self) -> int: ...

    @property
    def unknown(self) -> int: ...

    @property
    def valid(self) -> bool: ...