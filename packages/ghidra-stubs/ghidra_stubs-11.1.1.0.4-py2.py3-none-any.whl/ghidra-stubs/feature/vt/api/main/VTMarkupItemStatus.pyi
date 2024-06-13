from typing import List
from typing import overload
import ghidra.feature.vt.api.main
import java.lang
import java.util


class VTMarkupItemStatus(java.lang.Enum):
    ADDED: ghidra.feature.vt.api.main.VTMarkupItemStatus
    CONFLICT: ghidra.feature.vt.api.main.VTMarkupItemStatus
    DONT_CARE: ghidra.feature.vt.api.main.VTMarkupItemStatus
    DONT_KNOW: ghidra.feature.vt.api.main.VTMarkupItemStatus
    FAILED_APPLY: ghidra.feature.vt.api.main.VTMarkupItemStatus
    REJECTED: ghidra.feature.vt.api.main.VTMarkupItemStatus
    REPLACED: ghidra.feature.vt.api.main.VTMarkupItemStatus
    SAME: ghidra.feature.vt.api.main.VTMarkupItemStatus
    UNAPPLIED: ghidra.feature.vt.api.main.VTMarkupItemStatus







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def getDescription(self) -> unicode: ...

    def hashCode(self) -> int: ...

    def isAppliable(self) -> bool: ...

    def isDefault(self) -> bool: ...

    def isUnappliable(self) -> bool: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.feature.vt.api.main.VTMarkupItemStatus: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.feature.vt.api.main.VTMarkupItemStatus]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def appliable(self) -> bool: ...

    @property
    def default(self) -> bool: ...

    @property
    def description(self) -> unicode: ...

    @property
    def unappliable(self) -> bool: ...