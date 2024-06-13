from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.objc2
import ghidra.program.model.data
import ghidra.program.model.symbol
import java.lang


class ObjectiveC2_InstanceVariableList(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    NAME: unicode = u'ivar_list_t'
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



    def applyTo(self, namespace: ghidra.program.model.symbol.Namespace) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getCount(self) -> long: ...

    def getEntsize(self) -> long: ...

    def getIndex(self) -> long: ...

    def getIvars(self) -> List[ghidra.app.util.bin.format.objc2.ObjectiveC2_InstanceVariable]: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    @staticmethod
    def toGenericDataType() -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def count(self) -> long: ...

    @property
    def entsize(self) -> long: ...

    @property
    def index(self) -> long: ...

    @property
    def ivars(self) -> List[object]: ...