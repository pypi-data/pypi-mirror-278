from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class FunctionTable(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    NAME: unicode = u'MINIDUMP_FUNCTION_TABLE'
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

    def getBaseAddress(self) -> long: ...

    def getClass(self) -> java.lang.Class: ...

    def getEntryCount(self) -> int: ...

    def getMaximumAddress(self) -> long: ...

    def getMinimumAddress(self) -> long: ...

    def getSizeOfAlignPad(self) -> int: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setBaseAddress(self, __a0: long) -> None: ...

    def setEntryCount(self, __a0: int) -> None: ...

    def setMaximumAddress(self, __a0: long) -> None: ...

    def setMinimumAddress(self, __a0: long) -> None: ...

    def setSizeOfAlignPad(self, __a0: int) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def baseAddress(self) -> long: ...

    @baseAddress.setter
    def baseAddress(self, value: long) -> None: ...

    @property
    def entryCount(self) -> int: ...

    @entryCount.setter
    def entryCount(self, value: int) -> None: ...

    @property
    def maximumAddress(self) -> long: ...

    @maximumAddress.setter
    def maximumAddress(self, value: long) -> None: ...

    @property
    def minimumAddress(self) -> long: ...

    @minimumAddress.setter
    def minimumAddress(self, value: long) -> None: ...

    @property
    def sizeOfAlignPad(self) -> int: ...

    @sizeOfAlignPad.setter
    def sizeOfAlignPad(self, value: int) -> None: ...