from typing import overload
import java.lang


class CrushedPNGConstants(object):
    ADAM7_INTERLACE: int = 1
    COL_INCREMENT: List[int]
    GENERIC_CHUNK_SIZE: int = 12
    IDAT_CHUNK: List[int]
    IEND_CHUNK: List[int]
    IEND_STRING: unicode = u'IEND'
    IHDR_CHUNK: List[int]
    IHDR_CHUNK_DATA_SIZE: int = 13
    IHDR_STRING: unicode = u'IHDR'
    INITIAL_REPACK_SIZE: int = 65536
    INSERTED_IOS_CHUNK: List[int]
    INTERLACE_NONE: int = 0
    ROW_INCREMENT: List[int]
    SIGNATURE_BYTES: List[int]
    STARTING_COL: List[int]
    STARTING_ROW: List[int]



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

