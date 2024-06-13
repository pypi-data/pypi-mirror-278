from typing import List
from typing import overload
import ghidra.app.plugin.core.functiongraph.graph
import java.lang
import java.util


class FGVertexType(java.lang.Enum):
    BODY: ghidra.app.plugin.core.functiongraph.graph.FGVertexType
    ENTRY: ghidra.app.plugin.core.functiongraph.graph.FGVertexType
    EXIT: ghidra.app.plugin.core.functiongraph.graph.FGVertexType
    GROUP: ghidra.app.plugin.core.functiongraph.graph.FGVertexType
    SINGLETON: ghidra.app.plugin.core.functiongraph.graph.FGVertexType







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def isEntry(self) -> bool: ...

    def isExit(self) -> bool: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.app.plugin.core.functiongraph.graph.FGVertexType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.plugin.core.functiongraph.graph.FGVertexType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def entry(self) -> bool: ...

    @property
    def exit(self) -> bool: ...