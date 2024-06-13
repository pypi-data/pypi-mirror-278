from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class AoutHeader(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SIZEOF: int = 28
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getEntry(self) -> int: ...

    def getInitializedDataSize(self) -> int: ...

    def getInitializedDataStart(self) -> int: ...

    def getMagic(self) -> int: ...

    def getTextSize(self) -> int: ...

    def getTextStart(self) -> int: ...

    def getUninitializedDataSize(self) -> int: ...

    def getVersionStamp(self) -> int: ...

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
    def entry(self) -> int: ...

    @property
    def initializedDataSize(self) -> int: ...

    @property
    def initializedDataStart(self) -> int: ...

    @property
    def magic(self) -> int: ...

    @property
    def textSize(self) -> int: ...

    @property
    def textStart(self) -> int: ...

    @property
    def uninitializedDataSize(self) -> int: ...

    @property
    def versionStamp(self) -> int: ...