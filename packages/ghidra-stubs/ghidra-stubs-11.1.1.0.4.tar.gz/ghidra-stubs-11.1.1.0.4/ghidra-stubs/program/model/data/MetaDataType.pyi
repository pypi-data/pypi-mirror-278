from typing import List
from typing import overload
import ghidra.program.model.data
import java.lang
import java.util


class MetaDataType(java.lang.Enum):
    ARRAY: ghidra.program.model.data.MetaDataType
    BOOL: ghidra.program.model.data.MetaDataType
    CODE: ghidra.program.model.data.MetaDataType
    FLOAT: ghidra.program.model.data.MetaDataType
    INT: ghidra.program.model.data.MetaDataType
    PTR: ghidra.program.model.data.MetaDataType
    STRUCT: ghidra.program.model.data.MetaDataType
    UINT: ghidra.program.model.data.MetaDataType
    UNKNOWN: ghidra.program.model.data.MetaDataType
    VOID: ghidra.program.model.data.MetaDataType







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    @staticmethod
    def getMeta(__a0: ghidra.program.model.data.DataType) -> ghidra.program.model.data.MetaDataType: ...

    @staticmethod
    def getMostSpecificDataType(__a0: ghidra.program.model.data.DataType, __a1: ghidra.program.model.data.DataType) -> ghidra.program.model.data.DataType: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.program.model.data.MetaDataType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.program.model.data.MetaDataType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

