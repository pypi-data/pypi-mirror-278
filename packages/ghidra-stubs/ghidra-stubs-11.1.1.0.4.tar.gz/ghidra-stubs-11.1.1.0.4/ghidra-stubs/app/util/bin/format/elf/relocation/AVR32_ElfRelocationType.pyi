from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class AVR32_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    DT_AVR32_GOTSZ: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    EF_AVR32_LINKRELAX: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    EF_AVR32_PIC: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_10UW_PCREL: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_11H_PCREL: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_14UW_PCREL: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_16: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_16B_PCREL: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_16N_PCREL: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_16S: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_16U: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_16_CP: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_16_PCREL: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_18W_PCREL: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_21S: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_22H_PCREL: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_32: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_32_CPENT: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_32_PCREL: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_8: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_8S: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_8S_EXT: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_8_PCREL: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_9H_PCREL: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_9UW_PCREL: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_9W_CP: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_ALIGN: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_CPCALL: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_DIFF16: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_DIFF32: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_DIFF8: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_GLOB_DAT: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_GOT16: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_GOT16S: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_GOT18SW: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_GOT21S: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_GOT32: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_GOT7UW: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_GOT8: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_GOTCALL: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_GOTPC: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_HI16: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_JMP_SLOT: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_LDA_GOT: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_LO16: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_NONE: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_NUM: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType
    R_AVR32_RELATIVE: ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.AVR32_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

