from typing import List
from typing import overload
import ghidra.app.util.bin.format.coff
import ghidra.program.model.data
import java.lang


class CoffSymbolAuxFunction(object, ghidra.app.util.bin.format.coff.CoffSymbolAux):
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

    def getFilePointerToLineNumber(self) -> int: ...

    def getNextEntryIndex(self) -> int: ...

    def getSize(self) -> int: ...

    def getTagIndex(self) -> int: ...

    def getUnused(self) -> List[int]: ...

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
    def filePointerToLineNumber(self) -> int: ...

    @property
    def nextEntryIndex(self) -> int: ...

    @property
    def size(self) -> int: ...

    @property
    def tagIndex(self) -> int: ...

    @property
    def unused(self) -> List[int]: ...