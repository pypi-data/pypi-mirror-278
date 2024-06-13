from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class Module(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    NAME: unicode = u'MODULE_'
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

    def getModuleBase(self) -> long: ...

    def getModuleName(self) -> unicode: ...

    def getModuleNameLength(self) -> int: ...

    def getModuleSize(self) -> long: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setModuleBase(self, __a0: long) -> None: ...

    def setModuleName(self, __a0: unicode) -> None: ...

    def setModuleNameLength(self, __a0: int) -> None: ...

    def setModuleSize(self, __a0: long) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def moduleBase(self) -> long: ...

    @moduleBase.setter
    def moduleBase(self, value: long) -> None: ...

    @property
    def moduleName(self) -> unicode: ...

    @moduleName.setter
    def moduleName(self, value: unicode) -> None: ...

    @property
    def moduleNameLength(self) -> int: ...

    @moduleNameLength.setter
    def moduleNameLength(self, value: int) -> None: ...

    @property
    def moduleSize(self) -> long: ...

    @moduleSize.setter
    def moduleSize(self, value: long) -> None: ...