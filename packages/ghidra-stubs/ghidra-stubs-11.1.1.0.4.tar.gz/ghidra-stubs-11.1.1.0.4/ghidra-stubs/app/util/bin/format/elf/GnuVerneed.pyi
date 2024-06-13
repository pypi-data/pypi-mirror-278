from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class GnuVerneed(object, ghidra.app.util.bin.StructConverter):
    """
    Version dependency section.
 
     typedef struct {
       Elf32_Half	vn_version;		//Version of structure
       Elf32_Half	vn_cnt;			//Number of associated aux entries
       Elf32_Word	vn_file;		//Offset of filename for this dependency
       Elf32_Word	vn_aux;			//Offset in bytes to vernaux array
       Elf32_Word	vn_next;		//Offset in bytes to next verneed entry
     } Elf32_Verneed;
 
     typedef struct {
       Elf64_Half	vn_version;		//Version of structure
       Elf64_Half	vn_cnt;			//Number of associated aux entries
       Elf64_Word	vn_file;		//Offset of filename for this dependency
       Elf64_Word	vn_aux;			//Offset in bytes to vernaux array
       Elf64_Word	vn_next;		//Offset in bytes to next verneed entry
     } Elf64_Verneed;
 
 
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

    def getAux(self) -> int: ...

    def getClass(self) -> java.lang.Class: ...

    def getCnt(self) -> int: ...

    def getFile(self) -> int: ...

    def getNext(self) -> int: ...

    def getVersion(self) -> int: ...

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
    def aux(self) -> int: ...

    @property
    def cnt(self) -> int: ...

    @property
    def file(self) -> int: ...

    @property
    def next(self) -> int: ...

    @property
    def version(self) -> int: ...