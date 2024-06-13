from typing import List
from typing import overload
import ghidra.app.util.bin
import java.io
import java.lang


class ZLIB(object):
    ZLIB_COMPRESSION_BEST: List[int]
    ZLIB_COMPRESSION_DEFAULT: List[int]
    ZLIB_COMPRESSION_NO_LOW: List[int]



    def __init__(self): ...



    @overload
    def compress(self, __a0: List[int]) -> java.io.ByteArrayOutputStream: ...

    @overload
    def compress(self, __a0: bool, __a1: List[int]) -> java.io.ByteArrayOutputStream: ...

    @overload
    def decompress(self, __a0: java.io.InputStream, __a1: int) -> java.io.ByteArrayOutputStream: ...

    @overload
    def decompress(self, __a0: java.io.InputStream, __a1: int, __a2: bool) -> java.io.ByteArrayOutputStream: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    @staticmethod
    def isZLIB(__a0: ghidra.app.util.bin.ByteProvider) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

