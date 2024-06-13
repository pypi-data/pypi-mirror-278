from typing import List
from typing import overload
import generic.jar
import ghidra.program.model.listing
import java.lang


class DataTypeArchiveUtility(object):
    GHIDRA_ARCHIVES: java.util.Map







    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def findArchiveFile(__a0: unicode) -> generic.jar.ResourceFile: ...

    @staticmethod
    def getArchiveList(__a0: ghidra.program.model.listing.Program) -> List[object]: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getRemappedArchiveName(__a0: unicode) -> unicode: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

