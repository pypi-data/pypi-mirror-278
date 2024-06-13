from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.macho.commands
import ghidra.program.model.data
import java.lang


class DynamicLibrary(object, ghidra.app.util.bin.StructConverter):
    """
    Represents a dylib structure.
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



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader, command: ghidra.app.util.bin.format.macho.commands.LoadCommand): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getCompatibilityVersion(self) -> int: ...

    def getCurrentVersion(self) -> int: ...

    def getName(self) -> ghidra.app.util.bin.format.macho.commands.LoadCommandString: ...

    def getTimestamp(self) -> int: ...

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
    def compatibilityVersion(self) -> int: ...

    @property
    def currentVersion(self) -> int: ...

    @property
    def name(self) -> ghidra.app.util.bin.format.macho.commands.LoadCommandString: ...

    @property
    def timestamp(self) -> int: ...