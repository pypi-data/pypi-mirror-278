from typing import List
from typing import overload
import ghidra.app.util.demangler
import ghidra.program.model.data
import java.lang


class SwiftDataTypeUtils(object):
    SWIFT_CATEGORY: ghidra.program.model.data.CategoryPath



    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def extractParameters(__a0: ghidra.app.util.demangler.Demangled) -> List[object]: ...

    @staticmethod
    def getCategoryPath(__a0: ghidra.app.util.demangler.Demangled) -> ghidra.program.model.data.CategoryPath: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getSwiftNamespace() -> ghidra.app.util.demangler.Demangled: ...

    def hashCode(self) -> int: ...

    @staticmethod
    def isSwiftNamespace(__a0: ghidra.app.util.demangler.Demangled) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

