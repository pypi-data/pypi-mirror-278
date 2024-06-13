from typing import List
from typing import overload
import ghidra.debug.api.action
import ghidra.framework.plugintool
import java.lang
import java.util


class BasicLocationTrackingSpecFactory(object, ghidra.debug.api.action.LocationTrackingSpecFactory):
    ALL: List[object]
    BY_CONFIG_NAME: java.util.Map



    def __init__(self): ...



    @staticmethod
    def allSuggested(__a0: ghidra.framework.plugintool.PluginTool) -> java.util.Map: ...

    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def fromConfigName(__a0: unicode) -> ghidra.debug.api.action.LocationTrackingSpec: ...

    def getClass(self) -> java.lang.Class: ...

    def getSuggested(self, __a0: ghidra.framework.plugintool.PluginTool) -> List[object]: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parseSpec(self, __a0: unicode) -> ghidra.debug.api.action.LocationTrackingSpec: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

