from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.objectiveC
import ghidra.program.model.data
import java.lang


class ObjectiveC1_Category(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SIZEOF: long = 0x0L
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType



    def __init__(self, state: ghidra.app.util.bin.format.objectiveC.ObjectiveC1_State, reader: ghidra.app.util.bin.BinaryReader): ...



    def applyTo(self) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getCategoryName(self) -> unicode: ...

    def getClass(self) -> java.lang.Class: ...

    def getClassMethods(self) -> ghidra.app.util.bin.format.objectiveC.ObjectiveC1_MethodList: ...

    def getClassName(self) -> unicode: ...

    def getInstanceMethods(self) -> ghidra.app.util.bin.format.objectiveC.ObjectiveC1_MethodList: ...

    def getProtocols(self) -> ghidra.app.util.bin.format.objectiveC.ObjectiveC1_ProtocolList: ...

    def getUnknown0(self) -> int: ...

    def getUnknown1(self) -> int: ...

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
    def categoryName(self) -> unicode: ...

    @property
    def classMethods(self) -> ghidra.app.util.bin.format.objectiveC.ObjectiveC1_MethodList: ...

    @property
    def className(self) -> unicode: ...

    @property
    def instanceMethods(self) -> ghidra.app.util.bin.format.objectiveC.ObjectiveC1_MethodList: ...

    @property
    def protocols(self) -> ghidra.app.util.bin.format.objectiveC.ObjectiveC1_ProtocolList: ...

    @property
    def unknown0(self) -> int: ...

    @property
    def unknown1(self) -> int: ...