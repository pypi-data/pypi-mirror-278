from typing import List
from typing import overload
import ghidra.javaclass.flags
import java.lang
import java.util


class MethodsInfoAccessFlags(java.lang.Enum):
    ACC_ABSTRACT: ghidra.javaclass.flags.MethodsInfoAccessFlags
    ACC_BRIDGE: ghidra.javaclass.flags.MethodsInfoAccessFlags
    ACC_FINAL: ghidra.javaclass.flags.MethodsInfoAccessFlags
    ACC_NATIVE: ghidra.javaclass.flags.MethodsInfoAccessFlags
    ACC_PRIVATE: ghidra.javaclass.flags.MethodsInfoAccessFlags
    ACC_PROTECTED: ghidra.javaclass.flags.MethodsInfoAccessFlags
    ACC_PUBLIC: ghidra.javaclass.flags.MethodsInfoAccessFlags
    ACC_STATIC: ghidra.javaclass.flags.MethodsInfoAccessFlags
    ACC_STRICT: ghidra.javaclass.flags.MethodsInfoAccessFlags
    ACC_SYNCHRONIZED: ghidra.javaclass.flags.MethodsInfoAccessFlags
    ACC_SYNTHETIC: ghidra.javaclass.flags.MethodsInfoAccessFlags
    ACC_VARARGS: ghidra.javaclass.flags.MethodsInfoAccessFlags







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def getValue(self) -> int: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    @overload
    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def toString(__a0: int) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.javaclass.flags.MethodsInfoAccessFlags: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.javaclass.flags.MethodsInfoAccessFlags]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def value(self) -> int: ...