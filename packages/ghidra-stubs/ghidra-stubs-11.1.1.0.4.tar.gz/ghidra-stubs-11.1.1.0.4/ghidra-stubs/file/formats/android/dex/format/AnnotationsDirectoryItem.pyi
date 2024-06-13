from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.file.formats.android.dex.format
import ghidra.program.model.data
import java.lang


class AnnotationsDirectoryItem(object, ghidra.app.util.bin.StructConverter):
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



    def __init__(self, __a0: ghidra.app.util.bin.BinaryReader, __a1: ghidra.file.formats.android.dex.format.DexHeader): ...



    def equals(self, __a0: object) -> bool: ...

    def getAnnotatedMethodsSize(self) -> int: ...

    def getAnnotatedParametersSize(self) -> int: ...

    def getClass(self) -> java.lang.Class: ...

    def getClassAnnotations(self) -> ghidra.file.formats.android.dex.format.AnnotationSetItem: ...

    def getClassAnnotationsOffset(self) -> int: ...

    def getFieldAnnotations(self) -> List[object]: ...

    def getFieldsSize(self) -> int: ...

    def getMethodAnnotations(self) -> List[object]: ...

    def getParameterAnnotations(self) -> List[object]: ...

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
    def annotatedMethodsSize(self) -> int: ...

    @property
    def annotatedParametersSize(self) -> int: ...

    @property
    def classAnnotations(self) -> ghidra.file.formats.android.dex.format.AnnotationSetItem: ...

    @property
    def classAnnotationsOffset(self) -> int: ...

    @property
    def fieldAnnotations(self) -> List[object]: ...

    @property
    def fieldsSize(self) -> int: ...

    @property
    def methodAnnotations(self) -> List[object]: ...

    @property
    def parameterAnnotations(self) -> List[object]: ...