from typing import overload
import ghidra.program.model.lang.protorules.PrimitiveExtractor
import java.lang


class PrimitiveExtractor(object):





    class Primitive(object):
        dt: ghidra.program.model.data.DataType
        offset: int



        def __init__(self, __a0: ghidra.program.model.data.DataType, __a1: int): ...



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



    def __init__(self, dt: ghidra.program.model.data.DataType, unionIllegal: bool, offset: int, max: int):
        """
        @param dt is data-type extract from
        @param unionIllegal is true if unions encountered during extraction are considered illegal
        @param offset is the starting offset to associate with the data-type
        @param max is the maximum number of primitives to extract before giving up
        """
        ...



    def containsHoles(self) -> bool:
        """
        @return true if there is extra space in the data-type that is not alignment padding
        """
        ...

    def containsUnknown(self) -> bool:
        """
        @return true if any extracted element was unknown/undefined
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def get(self, i: int) -> ghidra.program.model.lang.protorules.PrimitiveExtractor.Primitive:
        """
        Get the i-th extracted primitive and its offset
        @param i is the index
        @return the primitive and offset
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def isAligned(self) -> bool:
        """
        @return true if all extracted elements are aligned
        """
        ...

    def isValid(self) -> bool:
        """
        @return true if all primitive elements were extracted
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def size(self) -> int:
        """
        @return the number of primitives extracted
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def aligned(self) -> bool: ...

    @property
    def valid(self) -> bool: ...