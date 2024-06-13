from typing import List
from typing import overload
import ghidra.service.graph
import java.lang
import java.util


class GraphLabelPosition(java.lang.Enum):
    CENTER: ghidra.service.graph.GraphLabelPosition
    EAST: ghidra.service.graph.GraphLabelPosition
    NORTH: ghidra.service.graph.GraphLabelPosition
    NORTHEAST: ghidra.service.graph.GraphLabelPosition
    NORTHWEST: ghidra.service.graph.GraphLabelPosition
    SOUTH: ghidra.service.graph.GraphLabelPosition
    SOUTHEAST: ghidra.service.graph.GraphLabelPosition
    SOUTHWEST: ghidra.service.graph.GraphLabelPosition
    WEST: ghidra.service.graph.GraphLabelPosition







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
    def valueOf(__a0: unicode) -> ghidra.service.graph.GraphLabelPosition: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.service.graph.GraphLabelPosition]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

