from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.file.formats.android.dex.format
import ghidra.program.model.data
import java.lang


class ClassDataItem(object, ghidra.app.util.bin.StructConverter):
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

    def getClass(self) -> java.lang.Class: ...

    def getDirectMethods(self) -> List[object]: ...

    def getDirectMethodsSize(self) -> int: ...

    def getInstanceFieldsSize(self) -> int: ...

    def getInstancesFields(self) -> List[object]: ...

    def getMethodByIndex(self, __a0: int) -> ghidra.file.formats.android.dex.format.EncodedMethod: ...

    def getStaticFields(self) -> List[object]: ...

    def getStaticFieldsSize(self) -> int: ...

    def getVirtualMethods(self) -> List[object]: ...

    def getVirtualMethodsSize(self) -> int: ...

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
    def directMethods(self) -> List[object]: ...

    @property
    def directMethodsSize(self) -> int: ...

    @property
    def instanceFieldsSize(self) -> int: ...

    @property
    def instancesFields(self) -> List[object]: ...

    @property
    def staticFields(self) -> List[object]: ...

    @property
    def staticFieldsSize(self) -> int: ...

    @property
    def virtualMethods(self) -> List[object]: ...

    @property
    def virtualMethodsSize(self) -> int: ...