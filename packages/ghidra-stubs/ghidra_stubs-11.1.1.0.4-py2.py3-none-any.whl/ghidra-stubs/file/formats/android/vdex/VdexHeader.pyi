from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.file.formats.android.vdex
import ghidra.file.formats.android.vdex.sections
import ghidra.program.model.data
import ghidra.util.task
import java.lang


class VdexHeader(object, ghidra.app.util.bin.StructConverter):
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

    def getDexChecksums(self) -> List[int]: ...

    def getDexHeaderList(self) -> List[object]: ...

    def getDexSectionHeader_002(self) -> ghidra.file.formats.android.vdex.sections.DexSectionHeader_002: ...

    def getDexStartOffset(self, __a0: int) -> long: ...

    def getMagic(self) -> unicode: ...

    def getQuickeningInfoSize(self) -> int: ...

    def getStringTable(self) -> ghidra.file.formats.android.vdex.VdexStringTable: ...

    def getVerifierDepsSize(self) -> int: ...

    def getVersion(self) -> unicode: ...

    def hashCode(self) -> int: ...

    def isDexHeaderEmbeddedInDataType(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parse(self, __a0: ghidra.app.util.bin.BinaryReader, __a1: ghidra.util.task.TaskMonitor) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def dexChecksums(self) -> List[int]: ...

    @property
    def dexHeaderEmbeddedInDataType(self) -> bool: ...

    @property
    def dexHeaderList(self) -> List[object]: ...

    @property
    def dexSectionHeader_002(self) -> ghidra.file.formats.android.vdex.sections.DexSectionHeader_002: ...

    @property
    def magic(self) -> unicode: ...

    @property
    def quickeningInfoSize(self) -> int: ...

    @property
    def stringTable(self) -> ghidra.file.formats.android.vdex.VdexStringTable: ...

    @property
    def verifierDepsSize(self) -> int: ...

    @property
    def version(self) -> unicode: ...