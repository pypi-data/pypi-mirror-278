from typing import List
from typing import overload
import ghidra.dbg.target
import ghidra.program.model.lang
import ghidra.util.classfinder
import java.lang
import java.util


class DebuggerMappingOpinion(ghidra.util.classfinder.ExtensionPoint, object):
    HIGHEST_CONFIDENCE_FIRST: java.util.Comparator







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getEndian(__a0: ghidra.dbg.target.TargetEnvironment) -> ghidra.program.model.lang.Endian: ...

    def getOffers(self, __a0: ghidra.dbg.target.TargetObject, __a1: bool) -> java.util.Set: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def offersForEnv(self, __a0: ghidra.dbg.target.TargetEnvironment, __a1: ghidra.dbg.target.TargetObject, __a2: bool) -> java.util.Set: ...

    @staticmethod
    def queryOpinions(__a0: ghidra.dbg.target.TargetObject, __a1: bool) -> List[object]: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

