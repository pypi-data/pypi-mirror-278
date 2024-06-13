from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class TriageDataBlock(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    NAME: unicode = u'_TRIAGE_DATA_BLOCK'
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

    def getAddress(self) -> long: ...

    def getClass(self) -> java.lang.Class: ...

    def getOffset(self) -> long: ...

    def getSize(self) -> long: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setAddress(self, __a0: long) -> None: ...

    def setOffset(self, __a0: long) -> None: ...

    def setSize(self, __a0: long) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def address(self) -> long: ...

    @address.setter
    def address(self, value: long) -> None: ...

    @property
    def offset(self) -> long: ...

    @offset.setter
    def offset(self, value: long) -> None: ...

    @property
    def size(self) -> long: ...

    @size.setter
    def size(self, value: long) -> None: ...