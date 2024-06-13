from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.file.formats.dump
import ghidra.program.model.data
import java.lang


class CvRecord(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    NAME: unicode = u'MINIDUMP_CV_RECORD'
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

    @staticmethod
    def getNameLength(__a0: ghidra.file.formats.dump.DumpFileReader, __a1: long) -> int: ...

    def getPdbAge(self) -> int: ...

    def getPdbFormat(self) -> int: ...

    def getPdbName(self) -> List[int]: ...

    def getPdbSigGUID(self) -> List[int]: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setPdbAge(self, __a0: int) -> None: ...

    def setPdbFormat(self, __a0: int) -> None: ...

    def setPdbName(self, __a0: int, __a1: int) -> None: ...

    def setPdbSigGUID(self, __a0: int, __a1: int) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def pdbAge(self) -> int: ...

    @pdbAge.setter
    def pdbAge(self, value: int) -> None: ...

    @property
    def pdbFormat(self) -> int: ...

    @pdbFormat.setter
    def pdbFormat(self, value: int) -> None: ...

    @property
    def pdbName(self) -> List[int]: ...

    @property
    def pdbSigGUID(self) -> List[int]: ...