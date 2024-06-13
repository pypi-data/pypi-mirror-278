from typing import List
from typing import overload
import ghidra.app.util.bin.format.pdb2.pdbreader.type
import java.lang
import java.util


class VtShapeDescriptorMsProperty(java.lang.Enum):
    FAR: ghidra.app.util.bin.format.pdb2.pdbreader.type.VtShapeDescriptorMsProperty
    FAR32: ghidra.app.util.bin.format.pdb2.pdbreader.type.VtShapeDescriptorMsProperty
    META: ghidra.app.util.bin.format.pdb2.pdbreader.type.VtShapeDescriptorMsProperty
    NEAR: ghidra.app.util.bin.format.pdb2.pdbreader.type.VtShapeDescriptorMsProperty
    NEAR32: ghidra.app.util.bin.format.pdb2.pdbreader.type.VtShapeDescriptorMsProperty
    OUTER: ghidra.app.util.bin.format.pdb2.pdbreader.type.VtShapeDescriptorMsProperty
    THIN: ghidra.app.util.bin.format.pdb2.pdbreader.type.VtShapeDescriptorMsProperty
    UNUSED: ghidra.app.util.bin.format.pdb2.pdbreader.type.VtShapeDescriptorMsProperty
    label: unicode
    value: int







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def fromValue(__a0: int) -> ghidra.app.util.bin.format.pdb2.pdbreader.type.VtShapeDescriptorMsProperty: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.pdb2.pdbreader.type.VtShapeDescriptorMsProperty: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.pdb2.pdbreader.type.VtShapeDescriptorMsProperty]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

