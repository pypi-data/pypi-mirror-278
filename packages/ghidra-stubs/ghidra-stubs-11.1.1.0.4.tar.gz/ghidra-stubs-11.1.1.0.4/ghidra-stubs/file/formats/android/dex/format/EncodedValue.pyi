from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.file.formats.android.dex.format
import ghidra.program.model.data
import java.lang


class EncodedValue(object, ghidra.app.util.bin.StructConverter):
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



    def __init__(self, __a0: ghidra.app.util.bin.BinaryReader): ...



    def equals(self, __a0: object) -> bool: ...

    def getAnnotation(self) -> ghidra.file.formats.android.dex.format.EncodedAnnotation: ...

    def getArray(self) -> ghidra.file.formats.android.dex.format.EncodedArray: ...

    def getClass(self) -> java.lang.Class: ...

    def getValueArgs(self) -> int: ...

    def getValueByte(self) -> int: ...

    def getValueBytes(self) -> List[int]: ...

    def getValueType(self) -> int: ...

    def hashCode(self) -> int: ...

    def isValueBoolean(self) -> bool: ...

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
    def annotation(self) -> ghidra.file.formats.android.dex.format.EncodedAnnotation: ...

    @property
    def array(self) -> ghidra.file.formats.android.dex.format.EncodedArray: ...

    @property
    def valueArgs(self) -> int: ...

    @property
    def valueBoolean(self) -> bool: ...

    @property
    def valueByte(self) -> int: ...

    @property
    def valueBytes(self) -> List[int]: ...

    @property
    def valueType(self) -> int: ...