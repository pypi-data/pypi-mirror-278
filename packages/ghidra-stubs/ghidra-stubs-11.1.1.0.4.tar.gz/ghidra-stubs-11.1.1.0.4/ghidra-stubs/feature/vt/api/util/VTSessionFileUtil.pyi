from typing import overload
import ghidra.framework.model
import java.lang


class VTSessionFileUtil(object):








    @staticmethod
    def canUpdate(__a0: ghidra.framework.model.DomainFile) -> bool: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @staticmethod
    def validateDestinationProgramFile(__a0: ghidra.framework.model.DomainFile, __a1: bool, __a2: bool) -> None: ...

    @staticmethod
    def validateSourceProgramFile(__a0: ghidra.framework.model.DomainFile, __a1: bool) -> None: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

