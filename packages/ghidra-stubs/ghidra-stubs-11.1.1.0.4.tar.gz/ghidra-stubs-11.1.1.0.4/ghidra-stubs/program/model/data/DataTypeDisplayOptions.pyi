from typing import overload
import java.lang


class DataTypeDisplayOptions(object):
    DEFAULT: ghidra.program.model.data.DataTypeDisplayOptions
    MAX_LABEL_STRING_LENGTH: int = 32







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getLabelStringLength(self) -> int: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    def useAbbreviatedForm(self) -> bool: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def labelStringLength(self) -> int: ...