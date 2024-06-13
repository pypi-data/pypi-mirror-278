from typing import overload
import ghidra.app.util.bin.format.elf
import ghidra.app.util.bin.format.elf.relocation
import ghidra.app.util.importer
import ghidra.program.model.address
import ghidra.program.model.listing
import java.lang


class AARCH64_ElfRelocationHandler(ghidra.app.util.bin.format.elf.relocation.AbstractElfRelocationHandler):




    def __init__(self): ...



    @staticmethod
    def applyComponentOffsetPointer(__a0: ghidra.program.model.listing.Program, __a1: ghidra.program.model.address.Address, __a2: long) -> None: ...

    @staticmethod
    def bookmarkNoHandlerError(__a0: ghidra.program.model.listing.Program, __a1: ghidra.program.model.address.Address, __a2: int, __a3: int, __a4: unicode) -> None: ...

    @staticmethod
    def bookmarkUnsupportedRelr(__a0: ghidra.program.model.listing.Program, __a1: ghidra.program.model.address.Address, __a2: int, __a3: unicode) -> None: ...

    def canRelocate(self, __a0: ghidra.app.util.bin.format.elf.ElfHeader) -> bool: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getRelocationType(self, __a0: int) -> ghidra.app.util.bin.format.elf.relocation.ElfRelocationType: ...

    def getRelrRelocationType(self) -> int: ...

    def hashCode(self) -> int: ...

    @overload
    @staticmethod
    def markAsError(__a0: ghidra.program.model.listing.Program, __a1: ghidra.program.model.address.Address, __a2: long, __a3: unicode, __a4: unicode, __a5: ghidra.app.util.importer.MessageLog) -> None: ...

    @overload
    @staticmethod
    def markAsError(__a0: ghidra.program.model.listing.Program, __a1: ghidra.program.model.address.Address, __a2: unicode, __a3: unicode, __a4: unicode, __a5: ghidra.app.util.importer.MessageLog) -> None: ...

    @overload
    @staticmethod
    def markAsError(__a0: ghidra.program.model.listing.Program, __a1: ghidra.program.model.address.Address, __a2: int, __a3: int, __a4: unicode, __a5: unicode, __a6: ghidra.app.util.importer.MessageLog) -> None: ...

    @staticmethod
    def markAsUnhandled(__a0: ghidra.program.model.listing.Program, __a1: ghidra.program.model.address.Address, __a2: long, __a3: long, __a4: unicode, __a5: ghidra.app.util.importer.MessageLog) -> None: ...

    @overload
    @staticmethod
    def markAsWarning(__a0: ghidra.program.model.listing.Program, __a1: ghidra.program.model.address.Address, __a2: unicode, __a3: unicode, __a4: ghidra.app.util.importer.MessageLog) -> None: ...

    @overload
    @staticmethod
    def markAsWarning(__a0: ghidra.program.model.listing.Program, __a1: ghidra.program.model.address.Address, __a2: unicode, __a3: unicode, __a4: int, __a5: unicode, __a6: ghidra.app.util.importer.MessageLog) -> None: ...

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
    def warnExternalOffsetRelocation(__a0: ghidra.program.model.listing.Program, __a1: ghidra.program.model.address.Address, __a2: ghidra.program.model.address.Address, __a3: unicode, __a4: long, __a5: ghidra.app.util.importer.MessageLog) -> None: ...

    @property
    def relrRelocationType(self) -> int: ...