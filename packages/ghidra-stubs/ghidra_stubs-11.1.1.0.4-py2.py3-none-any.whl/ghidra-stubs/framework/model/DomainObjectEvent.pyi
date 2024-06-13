from typing import List
from typing import overload
import ghidra.framework.model
import java.lang
import java.util


class DomainObjectEvent(java.lang.Enum, ghidra.framework.model.EventType):
    CLOSED: ghidra.framework.model.DomainObjectEvent
    ERROR: ghidra.framework.model.DomainObjectEvent
    FILE_CHANGED: ghidra.framework.model.DomainObjectEvent
    PROPERTY_CHANGED: ghidra.framework.model.DomainObjectEvent
    RENAMED: ghidra.framework.model.DomainObjectEvent
    RESTORED: ghidra.framework.model.DomainObjectEvent
    SAVED: ghidra.framework.model.DomainObjectEvent







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def getId(self) -> int: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.framework.model.DomainObjectEvent: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.framework.model.DomainObjectEvent]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def id(self) -> int: ...