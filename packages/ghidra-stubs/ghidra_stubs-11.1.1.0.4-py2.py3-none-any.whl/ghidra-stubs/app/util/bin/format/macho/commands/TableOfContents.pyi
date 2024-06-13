from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class TableOfContents(object, ghidra.app.util.bin.StructConverter):
    """
    Represents a dylib_table_of_contents structure.
    """

    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getModuleIndex(self) -> int:
        """
        An index into the module table indicating the module in which this defined
         external symbol is defined.
        @return an index into the module table
        """
        ...

    def getSymbolIndex(self) -> int:
        """
        An index into the symbol table indicating the defined external symbols
         to which this entry refers.
        @return an index into the symbol table
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
    def moduleIndex(self) -> int: ...

    @property
    def symbolIndex(self) -> int: ...