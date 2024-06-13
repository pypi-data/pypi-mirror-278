from typing import overload
import java.lang
import java.util
import java.util.function


class DataTypeObjectComparator(object, java.util.Comparator):
    """
    DataTypeObjectComparator provides the preferred named-based comparison of data types
     using the DataTypeNameComparator allowing a mix of DataType and/or String
     names to be compared.
    """

    INSTANCE: ghidra.program.model.data.DataTypeObjectComparator



    def __init__(self): ...



    def compare(self, o1: object, o2: object) -> int:
        """
        Compare two data type names
        @param o1 the first {@link DataType} or {@link String} name to be compared.
        @param o2 the second {@link DataType} or {@link String} name to be compared.
        @return a negative integer, zero, or a positive integer as the
                 first argument is less than, equal to, or greater than the
                 second.
        @throws IllegalArgumentException if object types other than {@link DataType} or 
         {@link String} are compared.
        """
        ...

    @overload
    @staticmethod
    def comparing(__a0: java.util.function.Function) -> java.util.Comparator: ...

    @overload
    @staticmethod
    def comparing(__a0: java.util.function.Function, __a1: java.util.Comparator) -> java.util.Comparator: ...

    @staticmethod
    def comparingDouble(__a0: java.util.function.ToDoubleFunction) -> java.util.Comparator: ...

    @staticmethod
    def comparingInt(__a0: java.util.function.ToIntFunction) -> java.util.Comparator: ...

    @staticmethod
    def comparingLong(__a0: java.util.function.ToLongFunction) -> java.util.Comparator: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    @staticmethod
    def naturalOrder() -> java.util.Comparator: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def nullsFirst(__a0: java.util.Comparator) -> java.util.Comparator: ...

    @staticmethod
    def nullsLast(__a0: java.util.Comparator) -> java.util.Comparator: ...

    @staticmethod
    def reverseOrder() -> java.util.Comparator: ...

    def reversed(self) -> java.util.Comparator: ...

    @overload
    def thenComparing(self, __a0: java.util.Comparator) -> java.util.Comparator: ...

    @overload
    def thenComparing(self, __a0: java.util.function.Function) -> java.util.Comparator: ...

    @overload
    def thenComparing(self, __a0: java.util.function.Function, __a1: java.util.Comparator) -> java.util.Comparator: ...

    def thenComparingDouble(self, __a0: java.util.function.ToDoubleFunction) -> java.util.Comparator: ...

    def thenComparingInt(self, __a0: java.util.function.ToIntFunction) -> java.util.Comparator: ...

    def thenComparingLong(self, __a0: java.util.function.ToLongFunction) -> java.util.Comparator: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

