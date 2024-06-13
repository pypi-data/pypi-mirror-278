from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class TwoLevelHint(object, ghidra.app.util.bin.StructConverter):
    """
    Represents a twolevel_hint structure.
    """

    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SIZEOF: int = 4
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getSubImageIndex(self) -> int:
        """
        An index into the sub-images (sub-frameworks and sub-umbrellas list).
        @return index into the sub-images
        """
        ...

    def getTableOfContentsIndex(self) -> int:
        """
        An index into the library's table of contents.
        @return index into the library's table of contents
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def subImageIndex(self) -> int: ...

    @property
    def tableOfContentsIndex(self) -> int: ...