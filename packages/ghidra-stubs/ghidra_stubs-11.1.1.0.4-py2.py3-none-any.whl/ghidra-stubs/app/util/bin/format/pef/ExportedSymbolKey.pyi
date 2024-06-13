from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class ExportedSymbolKey(object, ghidra.app.util.bin.StructConverter):
    """
    See Apple's -- PEFBinaryFormat.h * Exported Symbol Hash Key
 
     struct PEFExportedSymbolKey {
         union {
             UInt32            fullHashWord;
             PEFSplitHashWord  splitHashWord;
         } u;
     };
 
 
     struct PEFSplitHashWord {
         UInt16  nameLength;
         UInt16  hashValue;
     };
 
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

    def getFullHashWord(self) -> int: ...

    def getHashValue(self) -> int: ...

    def getNameLength(self) -> int: ...

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
    def fullHashWord(self) -> int: ...

    @property
    def hashValue(self) -> int: ...

    @property
    def nameLength(self) -> int: ...