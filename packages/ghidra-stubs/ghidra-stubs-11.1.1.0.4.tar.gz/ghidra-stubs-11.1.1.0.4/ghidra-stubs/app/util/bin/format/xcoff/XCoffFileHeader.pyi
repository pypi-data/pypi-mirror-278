from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.xcoff
import ghidra.program.model.data
import java.lang


class XCoffFileHeader(object, ghidra.app.util.bin.StructConverter):
    """
    XCOFF File Header.
     Handles both 32 and 64 bit cases.
    """

    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SIZEOF: int = 20
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType



    def __init__(self, provider: ghidra.app.util.bin.ByteProvider): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getFlags(self) -> int: ...

    def getMagic(self) -> int: ...

    def getOptionalHeader(self) -> ghidra.app.util.bin.format.xcoff.XCoffOptionalHeader: ...

    def getOptionalHeaderSize(self) -> int: ...

    def getSectionCount(self) -> int: ...

    def getSymbolTableEntries(self) -> int: ...

    def getSymbolTablePointer(self) -> long: ...

    def getTimeStamp(self) -> int: ...

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
    def flags(self) -> int: ...

    @property
    def magic(self) -> int: ...

    @property
    def optionalHeader(self) -> ghidra.app.util.bin.format.xcoff.XCoffOptionalHeader: ...

    @property
    def optionalHeaderSize(self) -> int: ...

    @property
    def sectionCount(self) -> int: ...

    @property
    def symbolTableEntries(self) -> int: ...

    @property
    def symbolTablePointer(self) -> long: ...

    @property
    def timeStamp(self) -> int: ...