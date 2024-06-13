from typing import overload
import ghidra.app.util.bin
import ghidra.file.formats.android.dex.format
import ghidra.program.model.data
import java.lang


class ParameterAnnotationsItem(object, ghidra.app.util.bin.StructConverter):
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

    def getAnnotationSetReferenceList(self) -> ghidra.file.formats.android.dex.format.AnnotationSetReferenceList: ...

    def getAnnotationsOffset(self) -> int: ...

    def getClass(self) -> java.lang.Class: ...

    def getMethodIndex(self) -> int: ...

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
    def annotationSetReferenceList(self) -> ghidra.file.formats.android.dex.format.AnnotationSetReferenceList: ...

    @property
    def annotationsOffset(self) -> int: ...

    @property
    def methodIndex(self) -> int: ...