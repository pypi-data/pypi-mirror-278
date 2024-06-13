from typing import List
from typing import overload
import ghidra.feature.vt.api.impl
import ghidra.framework.model
import java.lang
import java.util


class VTEvent(java.lang.Enum, ghidra.framework.model.EventType):
    ASSOCIATION_ADDED: ghidra.feature.vt.api.impl.VTEvent
    ASSOCIATION_MARKUP_STATUS_CHANGED: ghidra.feature.vt.api.impl.VTEvent
    ASSOCIATION_REMOVED: ghidra.feature.vt.api.impl.VTEvent
    ASSOCIATION_STATUS_CHANGED: ghidra.feature.vt.api.impl.VTEvent
    MARKUP_ITEM_DESTINATION_CHANGED: ghidra.feature.vt.api.impl.VTEvent
    MARKUP_ITEM_STATUS_CHANGED: ghidra.feature.vt.api.impl.VTEvent
    MATCH_ADDED: ghidra.feature.vt.api.impl.VTEvent
    MATCH_DELETED: ghidra.feature.vt.api.impl.VTEvent
    MATCH_SET_ADDED: ghidra.feature.vt.api.impl.VTEvent
    MATCH_TAG_CHANGED: ghidra.feature.vt.api.impl.VTEvent
    TAG_ADDED: ghidra.feature.vt.api.impl.VTEvent
    TAG_REMOVED: ghidra.feature.vt.api.impl.VTEvent
    VOTE_COUNT_CHANGED: ghidra.feature.vt.api.impl.VTEvent







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
    def valueOf(__a0: unicode) -> ghidra.feature.vt.api.impl.VTEvent: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.feature.vt.api.impl.VTEvent]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def id(self) -> int: ...