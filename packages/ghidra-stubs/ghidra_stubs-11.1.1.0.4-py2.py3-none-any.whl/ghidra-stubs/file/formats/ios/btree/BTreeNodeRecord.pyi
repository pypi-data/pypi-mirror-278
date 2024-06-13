from typing import overload
import ghidra.app.util.bin
import ghidra.file.formats.ios.decmpfs
import ghidra.program.model.data
import java.lang


class BTreeNodeRecord(object, ghidra.app.util.bin.StructConverter):
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

    def getDecmpfsHeader(self) -> ghidra.file.formats.ios.decmpfs.DecmpfsHeader: ...

    def getFileID(self) -> int: ...

    def getRecordLength(self) -> int: ...

    def getRecordOffset(self) -> long: ...

    def getType(self) -> unicode: ...

    def getUnknown0(self) -> int: ...

    def getUnknown2(self) -> int: ...

    def getUnknown3(self) -> int: ...

    def getUnknown4(self) -> int: ...

    def getUnknown5(self) -> int: ...

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
    def decmpfsHeader(self) -> ghidra.file.formats.ios.decmpfs.DecmpfsHeader: ...

    @property
    def fileID(self) -> int: ...

    @property
    def recordLength(self) -> int: ...

    @property
    def recordOffset(self) -> long: ...

    @property
    def type(self) -> unicode: ...

    @property
    def unknown0(self) -> int: ...

    @property
    def unknown2(self) -> int: ...

    @property
    def unknown3(self) -> int: ...

    @property
    def unknown4(self) -> int: ...

    @property
    def unknown5(self) -> int: ...