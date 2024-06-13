from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.objc2
import ghidra.program.model.data
import java.lang


class ObjectiveC2_Class(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    NAME: unicode = u'class_t'
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType



    def __init__(self, state: ghidra.app.util.bin.format.objc2.ObjectiveC2_State, reader: ghidra.app.util.bin.BinaryReader): ...



    def applyTo(self) -> None: ...

    def equals(self, that: object) -> bool: ...

    def getCache(self) -> ghidra.app.util.bin.format.objc2.ObjectiveC2_Cache: ...

    def getClass(self) -> java.lang.Class: ...

    def getData(self) -> ghidra.app.util.bin.format.objc2.ObjectiveC2_ClassRW: ...

    def getISA(self) -> ghidra.app.util.bin.format.objc2.ObjectiveC2_Class: ...

    def getIndex(self) -> long: ...

    def getSuperClass(self) -> ghidra.app.util.bin.format.objc2.ObjectiveC2_Class: ...

    def getVTable(self) -> ghidra.app.util.bin.format.objc2.ObjectiveC2_Implementation: ...

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
    def ISA(self) -> ghidra.app.util.bin.format.objc2.ObjectiveC2_Class: ...

    @property
    def VTable(self) -> ghidra.app.util.bin.format.objc2.ObjectiveC2_Implementation: ...

    @property
    def cache(self) -> ghidra.app.util.bin.format.objc2.ObjectiveC2_Cache: ...

    @property
    def data(self) -> ghidra.app.util.bin.format.objc2.ObjectiveC2_ClassRW: ...

    @property
    def index(self) -> long: ...

    @property
    def superClass(self) -> ghidra.app.util.bin.format.objc2.ObjectiveC2_Class: ...