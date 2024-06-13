from typing import List
from typing import overload
import ghidra.app.util.bin.format.golang.rtti.types
import java.lang
import java.util


class GoKind(java.lang.Enum):
    Array: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Bool: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Chan: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Complex128: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Complex64: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    DIRECT_IFACE: int = 32
    Float32: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Float64: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Func: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    GC_PROG: int = 64
    Int: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Int16: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Int32: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Int64: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Int8: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Interface: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    KIND_MASK: int = 31
    Map: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Pointer: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Slice: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    String: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Struct: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Uint: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Uint16: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Uint32: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Uint64: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Uint8: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    Uintptr: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    UnsafePointer: ghidra.app.util.bin.format.golang.rtti.types.GoKind
    invalid: ghidra.app.util.bin.format.golang.rtti.types.GoKind







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    @staticmethod
    def parseByte(__a0: int) -> ghidra.app.util.bin.format.golang.rtti.types.GoKind: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.golang.rtti.types.GoKind: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.golang.rtti.types.GoKind]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

