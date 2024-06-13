from typing import overload
import java.lang


class BuiltinDBAdapter(object):
    """
    Database adapter for managing built-in data types.
    """





    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getRecordCount(self) -> int:
        """
        Get the number of built-in datatype records
        @return total number of composite records
        """
        ...

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

    @property
    def recordCount(self) -> int: ...