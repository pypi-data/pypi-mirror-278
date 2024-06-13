from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.file.formats.android.oat
import ghidra.file.formats.android.oat.bundle
import ghidra.program.model.data
import java.lang


class OatHeader(object, ghidra.app.util.bin.StructConverter):
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

    def getChecksum(self) -> int: ...

    def getClass(self) -> java.lang.Class: ...

    def getDexFileCount(self) -> int: ...

    def getExecutableOffset(self) -> int: ...

    def getInstructionSet(self) -> ghidra.file.formats.android.oat.OatInstructionSet: ...

    def getKeyValueStoreSize(self) -> int: ...

    def getMagic(self) -> unicode: ...

    def getOatDexFileList(self) -> List[object]: ...

    def getOatDexFilesOffset(self, __a0: ghidra.app.util.bin.BinaryReader) -> int: ...

    def getVersion(self) -> unicode: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parse(self, __a0: ghidra.app.util.bin.BinaryReader, __a1: ghidra.file.formats.android.oat.bundle.OatBundle) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def checksum(self) -> int: ...

    @property
    def dexFileCount(self) -> int: ...

    @property
    def executableOffset(self) -> int: ...

    @property
    def instructionSet(self) -> ghidra.file.formats.android.oat.OatInstructionSet: ...

    @property
    def keyValueStoreSize(self) -> int: ...

    @property
    def magic(self) -> unicode: ...

    @property
    def oatDexFileList(self) -> List[object]: ...

    @property
    def version(self) -> unicode: ...