from typing import List
from typing import overload
import ghidra.app.util.bin
import java.lang


class ProfileConstants(object):
    kDexMetadataProfileEntry: unicode = u'primary.prof'
    kProfileMagic: List[int]
    kProfileMagicLength: int = 4
    kProfileVersionForBootImage_012: List[int]
    kProfileVersionWithCounters: List[int]
    kProfileVersion_008: List[int]
    kProfileVersion_009: List[int]
    kProfileVersion_010: List[int]



    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    @staticmethod
    def isProfile(__a0: ghidra.app.util.bin.ByteProvider) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def toString(__a0: List[int]) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

