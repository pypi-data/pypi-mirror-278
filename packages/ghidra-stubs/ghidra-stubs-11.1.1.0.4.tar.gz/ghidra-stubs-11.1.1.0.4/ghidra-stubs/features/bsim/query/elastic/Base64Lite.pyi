from typing import overload
import java.lang


class Base64Lite(object):
    decode: List[int]
    encode: List[int]



    def __init__(self): ...



    @staticmethod
    def decodeLongBase64(__a0: unicode) -> long: ...

    @overload
    @staticmethod
    def encodeLongBase64(__a0: long) -> unicode: ...

    @overload
    @staticmethod
    def encodeLongBase64(__a0: java.lang.StringBuilder, __a1: long) -> None: ...

    @staticmethod
    def encodeLongBase64Padded(__a0: java.lang.StringBuilder, __a1: long) -> None: ...

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

