from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class MSP430X_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    R_MSP430X_10_PCREL: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430X_2X_PCREL: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430X_ABS16: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430X_ABS20_ADR_DST: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430X_ABS20_ADR_SRC: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430X_ABS20_EXT_DST: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430X_ABS20_EXT_ODST: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430X_ABS20_EXT_SRC: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430X_PCR16: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430X_PCR20_CALL: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430X_PCR20_EXT_DST: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430X_PCR20_EXT_ODST: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430X_PCR20_EXT_SRC: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430X_SET_ULEB128: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430X_SUB_ULEB128: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430X_SYM_DIFF: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430_ABS16: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430_ABS32: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430_ABS8: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430_ABS_HI16: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430_EHTYPE: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430_NONE: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430_PCR16: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType
    R_MSP430_PREL31: ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    def typeId(self) -> int: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.MSP430X_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

