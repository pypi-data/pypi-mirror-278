from typing import overload
import ghidra.app.util.bin.format.elf
import ghidra.app.util.bin.format.elf.relocation
import ghidra.app.util.importer
import ghidra.program.model.address
import ghidra.program.model.listing
import java.lang


class AbstractElfRelocationHandler(ghidra.app.util.bin.format.elf.relocation.ElfRelocationHandler):
    """
    ElfRelocationHandler provides the base class for processor specific
     ELF relocation handlers.  Implementations may only specify a public default constructor
     as they will be identified and instatiated by the ClassSearcher.  As such their
     name must end with "ElfRelocationHandler" (e.g., MyProc_ElfRelocationHandler).
    """









    @staticmethod
    def applyComponentOffsetPointer(program: ghidra.program.model.listing.Program, addr: ghidra.program.model.address.Address, componentOffset: long) -> None:
        """
        Apply a pointer-typedef with a specified component-offset if specified address
         is not contained within an execute block.
        @param program program
        @param addr address where data should be applied
        @param componentOffset component offset
        """
        ...

    @staticmethod
    def bookmarkNoHandlerError(program: ghidra.program.model.listing.Program, relocationAddress: ghidra.program.model.address.Address, typeId: int, symbolIndex: int, symbolName: unicode) -> None:
        """
        Generate error bookmark at relocationAddress indicating a missing relocation handler.
        @param program program
        @param relocationAddress relocation address to be bookmarked
        @param typeId relocation type ID value
        @param symbolIndex associated symbol index within symbol table (-1 to ignore)
        @param symbolName associated symbol name
        """
        ...

    @staticmethod
    def bookmarkUnsupportedRelr(program: ghidra.program.model.listing.Program, relocationAddress: ghidra.program.model.address.Address, symbolIndex: int, symbolName: unicode) -> None:
        """
        Generate error bookmark at relocationAddress indicating an unsupported RELR relocation.
        @param program program
        @param relocationAddress relocation address to be bookmarked
        @param symbolIndex associated symbol index within symbol table (-1 to ignore)
        @param symbolName associated symbol name
        """
        ...

    def canRelocate(self, elf: ghidra.app.util.bin.format.elf.ElfHeader) -> bool: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getRelocationType(self, typeId: int) -> object:
        """
        Get the relocation type enum object which corresponds to the specified type ID value.
        @param typeId relocation type ID value
        @return relocation type enum value or null if type not found or this handler was not
         constructed with a {@link ElfRelocationType} enum class.  The returned value may be
         safely cast to the relocation enum class specified during handler construction.
        """
        ...

    def getRelrRelocationType(self) -> int:
        """
        Get the architecture-specific relative relocation type which should be applied to 
         RELR relocations.  The default implementation returns 0 which indicates RELR is unsupported.
        @return RELR relocation type ID value
        """
        ...

    def hashCode(self) -> int: ...

    @overload
    @staticmethod
    def markAsError(program: ghidra.program.model.listing.Program, relocationAddress: ghidra.program.model.address.Address, typeId: long, symbolName: unicode, msg: unicode, log: ghidra.app.util.importer.MessageLog) -> None:
        """
        Generate error log entry and bookmark at relocationAddress
        @param program program
        @param relocationAddress relocation address to be bookmarked
        @param typeId relocation type ID value
        @param symbolName associated symbol name
        @param msg error messge
        @param log import log
        """
        ...

    @overload
    @staticmethod
    def markAsError(program: ghidra.program.model.listing.Program, relocationAddress: ghidra.program.model.address.Address, type: unicode, symbolName: unicode, msg: unicode, log: ghidra.app.util.importer.MessageLog) -> None:
        """
        Generate error log entry and bookmark at relocationAddress
        @param program program
        @param relocationAddress relocation address to be bookmarked
        @param type relocation type ID name
        @param symbolName associated symbol name
        @param msg additional error message
        @param log import log
        """
        ...

    @overload
    @staticmethod
    def markAsError(program: ghidra.program.model.listing.Program, relocationAddress: ghidra.program.model.address.Address, typeId: int, symbolIndex: int, symbolName: unicode, msg: unicode, log: ghidra.app.util.importer.MessageLog) -> None:
        """
        Generate error log entry and bookmark at relocationAddress
        @param program program
        @param relocationAddress relocation address to be bookmarked
        @param typeId relocation type
        @param symbolIndex associated symbol index within symbol table (-1 to ignore)
        @param symbolName associated symbol name
        @param msg error messge
        @param log import log
        """
        ...

    @staticmethod
    def markAsUnhandled(program: ghidra.program.model.listing.Program, relocationAddress: ghidra.program.model.address.Address, typeId: long, symbolIndex: long, symbolName: unicode, log: ghidra.app.util.importer.MessageLog) -> None:
        """
        Generate error log entry and bookmark at relocationAddress indicating 
         an unhandled relocation.
        @param program program
        @param relocationAddress relocation address to be bookmarked
        @param typeId relocation type ID value (limited to int value).
        @param symbolIndex associated symbol index within symbol table (limited to int value).
        @param symbolName associated symbol name
        @param log import log
        """
        ...

    @overload
    @staticmethod
    def markAsWarning(program: ghidra.program.model.listing.Program, relocationAddress: ghidra.program.model.address.Address, type: unicode, msg: unicode, log: ghidra.app.util.importer.MessageLog) -> None:
        """
        Generate warning log entry and bookmark at relocationAddress
        @param program program
        @param relocationAddress relocation address to be bookmarked
        @param type relocation type ID name
        @param msg message associated with warning
        @param log import log
        """
        ...

    @overload
    @staticmethod
    def markAsWarning(program: ghidra.program.model.listing.Program, relocationAddress: ghidra.program.model.address.Address, type: unicode, symbolName: unicode, symbolIndex: int, msg: unicode, log: ghidra.app.util.importer.MessageLog) -> None:
        """
        Generate warning log entry and bookmark at relocationAddress
        @param program program
        @param relocationAddress relocation address to be bookmarked
        @param type relocation type ID name
        @param symbolName symbol name
        @param symbolIndex symbol index (-1 to ignore)
        @param msg message associated with warning
        @param log import log
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @staticmethod
    def warnExternalOffsetRelocation(program: ghidra.program.model.listing.Program, relocationAddress: ghidra.program.model.address.Address, symbolAddr: ghidra.program.model.address.Address, symbolName: unicode, adjustment: long, log: ghidra.app.util.importer.MessageLog) -> None:
        """
        Determine if symbolAddr is contained within the EXTERNAL block with a non-zero adjustment.  
         If so, relocationAddress will be marked with a <code>EXTERNAL Data Elf Relocation with pointer-offset</code> 
         warning or error bookmark.  Bookmark and logged message will be conveyed as an error if 
         relocationAddress resides within an executable memory block.
         <br>
         NOTE: This method should only be invoked when the symbol offset will be adjusted with a non-zero 
         value (i.e., addend).
        @param program program
        @param relocationAddress relocation address to be bookmarked if EXTERNAL block relocation
        @param symbolAddr symbol address correspondng to relocation (may be null)
        @param symbolName symbol name (may not be null if symbolAddr is not null)
        @param adjustment relocation symbol offset adjustment/addend
        @param log import log
        """
        ...

