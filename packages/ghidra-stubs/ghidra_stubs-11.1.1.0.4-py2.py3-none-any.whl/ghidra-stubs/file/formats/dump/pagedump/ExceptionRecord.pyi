from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class ExceptionRecord(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    NAME: unicode = u'PAGEDUMP_EXCEPTION_RECORD'
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

    def getExceptionAddress(self) -> long: ...

    def getExceptionCode(self) -> int: ...

    def getExceptionFlags(self) -> int: ...

    def getExceptionRecord(self) -> long: ...

    def getNumberOfParameters(self) -> int: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setExceptionAddress(self, __a0: long) -> None: ...

    def setExceptionCode(self, __a0: int) -> None: ...

    def setExceptionFlags(self, __a0: int) -> None: ...

    def setExceptionRecord(self, __a0: long) -> None: ...

    def setNumberOfParameters(self, __a0: int) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def exceptionAddress(self) -> long: ...

    @exceptionAddress.setter
    def exceptionAddress(self, value: long) -> None: ...

    @property
    def exceptionCode(self) -> int: ...

    @exceptionCode.setter
    def exceptionCode(self, value: int) -> None: ...

    @property
    def exceptionFlags(self) -> int: ...

    @exceptionFlags.setter
    def exceptionFlags(self, value: int) -> None: ...

    @property
    def exceptionRecord(self) -> long: ...

    @exceptionRecord.setter
    def exceptionRecord(self, value: long) -> None: ...

    @property
    def numberOfParameters(self) -> int: ...

    @numberOfParameters.setter
    def numberOfParameters(self, value: int) -> None: ...