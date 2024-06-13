from typing import overload
import java.lang


class CartV1Constants(object):
    ARC4_KEY_LENGTH: int = 16
    BLOCK_SIZE: int = 65536
    DEFAULT_ARC4_KEY: List[int]
    EXPECTED_HASHES: java.util.Map
    FOOTER_LENGTH: int = 28
    FOOTER_MAGIC: unicode = u'TRAC'
    FOOTER_ONLY_KEYS: java.util.Set
    FOOTER_RESERVED: long = 0x0L
    HEADER_LENGTH: int = 38
    HEADER_MAGIC: unicode = u'CART'
    HEADER_RESERVED: long = 0x0L
    HEADER_VERSION: int = 1
    MINIMUM_LENGTH: int = 66
    PRIVATE_ARC4_KEY_PLACEHOLDER: List[int]
    ZLIB_HEADER_BYTES: List[object]



    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

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

