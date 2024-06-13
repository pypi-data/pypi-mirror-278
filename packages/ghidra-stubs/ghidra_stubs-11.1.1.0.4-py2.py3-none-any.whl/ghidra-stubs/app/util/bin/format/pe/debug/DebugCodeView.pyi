from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.pdb
import ghidra.app.util.bin.format.pe.debug
import ghidra.program.model.data
import java.lang


class DebugCodeView(object, ghidra.app.util.bin.StructConverter):
    """
    A class to represent the code view debug information.
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

    def getDebugDirectory(self) -> ghidra.app.util.bin.format.pe.debug.DebugDirectory:
        """
        Returns the code view debug directory.
        @return the code view debug directory
        """
        ...

    def getDotNetPdbInfo(self) -> ghidra.app.util.bin.format.pdb.PdbInfoDotNet: ...

    def getPdbInfo(self) -> ghidra.app.util.bin.format.pdb.PdbInfoCodeView:
        """
        Returns the code view .PDB info.
        @return the code view .PDB info
        """
        ...

    def getSymbolTable(self) -> ghidra.app.util.bin.format.pe.debug.DebugCodeViewSymbolTable:
        """
        Returns the code view symbol table.
        @return the code view symbol table
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType:
        """
        @see ghidra.app.util.bin.StructConverter#toDataType()
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
    def debugDirectory(self) -> ghidra.app.util.bin.format.pe.debug.DebugDirectory: ...

    @property
    def dotNetPdbInfo(self) -> ghidra.app.util.bin.format.pdb.PdbInfoDotNet: ...

    @property
    def pdbInfo(self) -> ghidra.app.util.bin.format.pdb.PdbInfoCodeView: ...

    @property
    def symbolTable(self) -> ghidra.app.util.bin.format.pe.debug.DebugCodeViewSymbolTable: ...