from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.objectiveC
import ghidra.program.model.data
import java.lang


class ObjectiveC1_SymbolTable(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    NAME: unicode = u'objc_symtab'
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType







    def applyTo(self) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getCategories(self) -> List[ghidra.app.util.bin.format.objectiveC.ObjectiveC1_Category]: ...

    def getCategoryDefinitionCount(self) -> int: ...

    def getClass(self) -> java.lang.Class: ...

    def getClassDefinitionCount(self) -> int: ...

    def getClasses(self) -> List[ghidra.app.util.bin.format.objectiveC.ObjectiveC1_Class]: ...

    def getRefs(self) -> int: ...

    def getSelectorReferenceCount(self) -> int: ...

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
    def categories(self) -> List[object]: ...

    @property
    def categoryDefinitionCount(self) -> int: ...

    @property
    def classDefinitionCount(self) -> int: ...

    @property
    def classes(self) -> List[object]: ...

    @property
    def refs(self) -> int: ...

    @property
    def selectorReferenceCount(self) -> int: ...