from typing import List
from typing import overload
import ghidra.app.util.bin.format.golang.rtti
import java.lang
import java.util


class GoFuncID(java.lang.Enum):
    ABORT: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    ASMCGOCALL: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    ASYNCPREEMPT: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    CGOCALLBACK: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    DEBUGCALLV2: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    GCBGMARKWORKER: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    GOEXIT: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    GOGO: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    GOPANIC: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    HANDLEASYNCEVENT: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    MCALL: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    MORESTACK: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    MSTART: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    NORMAL: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    PANICWRAP: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    RT0_GO: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    RUNFINQ: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    RUNTIME_MAIN: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    SIGPANIC: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    SYSTEMSTACK: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    SYSTEMSTACK_SWITCH: ghidra.app.util.bin.format.golang.rtti.GoFuncID
    WRAPPER: ghidra.app.util.bin.format.golang.rtti.GoFuncID







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
    def parseIDByte(__a0: int) -> ghidra.app.util.bin.format.golang.rtti.GoFuncID: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.golang.rtti.GoFuncID: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.golang.rtti.GoFuncID]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

