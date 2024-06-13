from typing import overload
import java.lang
import java.util
import java.util.concurrent.locks
import java.util.stream


class StreamUtils(object):








    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    @staticmethod
    def iter(__a0: java.util.stream.Stream) -> java.lang.Iterable: ...

    @staticmethod
    def lock(__a0: java.util.concurrent.locks.Lock, __a1: java.util.stream.Stream) -> java.util.stream.Stream: ...

    @staticmethod
    def merge(__a0: java.util.Collection, __a1: java.util.Comparator) -> java.util.stream.Stream: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def sync(__a0: object, __a1: java.util.stream.Stream) -> java.util.stream.Stream: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

