from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class RelocationInfo(object, ghidra.app.util.bin.StructConverter):
    """
    Represents a relocation_info and scattered_relocation_info structure.
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



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader): ...



    def equals(self, __a0: object) -> bool: ...

    def getAddress(self) -> int: ...

    def getClass(self) -> java.lang.Class: ...

    def getLength(self) -> int: ...

    def getType(self) -> int: ...

    def getValue(self) -> int: ...

    def hashCode(self) -> int: ...

    def isExternal(self) -> bool: ...

    def isPcRelocated(self) -> bool: ...

    def isScattered(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    def toValues(self) -> List[long]:
        """
        Returns the values array for storage into the program's relocation table.
        @return the values array for storage into the program's relocation table
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def address(self) -> int: ...

    @property
    def external(self) -> bool: ...

    @property
    def length(self) -> int: ...

    @property
    def pcRelocated(self) -> bool: ...

    @property
    def scattered(self) -> bool: ...

    @property
    def type(self) -> int: ...

    @property
    def value(self) -> int: ...