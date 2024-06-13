from typing import overload
import ghidra.framework.model
import java.lang


class DomainObjectDisplayUtils(object):








    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getShortPath(df: ghidra.framework.model.DomainFile) -> unicode: ...

    @overload
    @staticmethod
    def getTabText(df: ghidra.framework.model.DomainFile) -> unicode: ...

    @overload
    @staticmethod
    def getTabText(object: ghidra.framework.model.DomainObject) -> unicode: ...

    @staticmethod
    def getToolTip(object: ghidra.framework.model.DomainObject) -> unicode: ...

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

