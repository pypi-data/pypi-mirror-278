from typing import List
from typing import overload
import ghidra.framework.options
import java.lang
import java.util


class OptionType(java.lang.Enum):
    ACTION_TRIGGER: ghidra.framework.options.OptionType
    BOOLEAN_TYPE: ghidra.framework.options.OptionType
    BYTE_ARRAY_TYPE: ghidra.framework.options.OptionType
    COLOR_TYPE: ghidra.framework.options.OptionType
    CUSTOM_TYPE: ghidra.framework.options.OptionType
    DATE_TYPE: ghidra.framework.options.OptionType
    DOUBLE_TYPE: ghidra.framework.options.OptionType
    ENUM_TYPE: ghidra.framework.options.OptionType
    FILE_TYPE: ghidra.framework.options.OptionType
    FLOAT_TYPE: ghidra.framework.options.OptionType
    FONT_TYPE: ghidra.framework.options.OptionType
    INT_TYPE: ghidra.framework.options.OptionType
    KEYSTROKE_TYPE: ghidra.framework.options.OptionType
    LONG_TYPE: ghidra.framework.options.OptionType
    NO_TYPE: ghidra.framework.options.OptionType
    STRING_TYPE: ghidra.framework.options.OptionType




    class ByteArrayStringAdapter(ghidra.framework.options.OptionType.StringAdapter):




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







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def convertObjectToString(self, __a0: object) -> unicode: ...

    def convertStringToObject(self, __a0: unicode) -> object: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    @staticmethod
    def getOptionType(__a0: object) -> ghidra.framework.options.OptionType: ...

    def getValueClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def isCompatible(self, __a0: object) -> bool: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.framework.options.OptionType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.framework.options.OptionType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def valueClass(self) -> java.lang.Class: ...