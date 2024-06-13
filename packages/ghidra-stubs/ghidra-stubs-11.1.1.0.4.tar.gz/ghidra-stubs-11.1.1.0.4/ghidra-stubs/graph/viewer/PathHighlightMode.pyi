from typing import List
from typing import overload
import ghidra.graph.viewer
import java.lang
import java.util


class PathHighlightMode(java.lang.Enum):
    ALLCYCLE: ghidra.graph.viewer.PathHighlightMode
    CYCLE: ghidra.graph.viewer.PathHighlightMode
    IN: ghidra.graph.viewer.PathHighlightMode
    INOUT: ghidra.graph.viewer.PathHighlightMode
    OFF: ghidra.graph.viewer.PathHighlightMode
    OUT: ghidra.graph.viewer.PathHighlightMode
    PATH: ghidra.graph.viewer.PathHighlightMode
    SCOPED_FORWARD: ghidra.graph.viewer.PathHighlightMode
    SCOPED_REVERSE: ghidra.graph.viewer.PathHighlightMode







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

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.graph.viewer.PathHighlightMode: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.graph.viewer.PathHighlightMode]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

