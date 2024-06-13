from typing import List
from typing import overload
import ghidra.app.plugin.core.debug.gui.memview
import java.awt
import java.lang
import java.util


class MemviewBoxType(java.lang.Enum):
    BREAKPOINT: ghidra.app.plugin.core.debug.gui.memview.MemviewBoxType
    HEAP_ALLOC: ghidra.app.plugin.core.debug.gui.memview.MemviewBoxType
    HEAP_CREATE: ghidra.app.plugin.core.debug.gui.memview.MemviewBoxType
    IMAGE: ghidra.app.plugin.core.debug.gui.memview.MemviewBoxType
    INSTRUCTIONS: ghidra.app.plugin.core.debug.gui.memview.MemviewBoxType
    MODULE: ghidra.app.plugin.core.debug.gui.memview.MemviewBoxType
    PERFINFO: ghidra.app.plugin.core.debug.gui.memview.MemviewBoxType
    POOL: ghidra.app.plugin.core.debug.gui.memview.MemviewBoxType
    PROCESS: ghidra.app.plugin.core.debug.gui.memview.MemviewBoxType
    READ_MEMORY: ghidra.app.plugin.core.debug.gui.memview.MemviewBoxType
    REGION: ghidra.app.plugin.core.debug.gui.memview.MemviewBoxType
    STACK: ghidra.app.plugin.core.debug.gui.memview.MemviewBoxType
    THREAD: ghidra.app.plugin.core.debug.gui.memview.MemviewBoxType
    VIRTUAL_ALLOC: ghidra.app.plugin.core.debug.gui.memview.MemviewBoxType
    WRITE_MEMORY: ghidra.app.plugin.core.debug.gui.memview.MemviewBoxType







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getColor(self) -> java.awt.Color: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.app.plugin.core.debug.gui.memview.MemviewBoxType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.plugin.core.debug.gui.memview.MemviewBoxType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def color(self) -> java.awt.Color: ...