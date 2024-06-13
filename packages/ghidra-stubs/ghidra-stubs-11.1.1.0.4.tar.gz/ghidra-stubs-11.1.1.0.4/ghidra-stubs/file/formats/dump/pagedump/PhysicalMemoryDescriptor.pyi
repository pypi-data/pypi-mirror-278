from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.file.formats.dump.pagedump
import ghidra.program.model.data
import java.lang


class PhysicalMemoryDescriptor(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    NAME: unicode = u'PAGEDUMP_PHYS_MEMORY_DESCRIPTOR'
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

    def getNumberOfPages(self) -> long: ...

    def getNumberOfRuns(self) -> int: ...

    def getRuns(self) -> List[ghidra.file.formats.dump.pagedump.PhysicalMemoryRun]: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setNumberOfPages(self, __a0: long) -> None: ...

    def setNumberOfRuns(self, __a0: int) -> None: ...

    def setRuns(self, __a0: ghidra.file.formats.dump.pagedump.PhysicalMemoryRun, __a1: int) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def numberOfPages(self) -> long: ...

    @numberOfPages.setter
    def numberOfPages(self, value: long) -> None: ...

    @property
    def numberOfRuns(self) -> int: ...

    @numberOfRuns.setter
    def numberOfRuns(self, value: int) -> None: ...

    @property
    def runs(self) -> List[ghidra.file.formats.dump.pagedump.PhysicalMemoryRun]: ...