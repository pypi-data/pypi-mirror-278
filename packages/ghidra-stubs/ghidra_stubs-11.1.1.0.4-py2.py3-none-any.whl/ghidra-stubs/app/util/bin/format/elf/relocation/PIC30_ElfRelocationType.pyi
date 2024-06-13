from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class PIC30_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    R_PIC30_16: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_32: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_8: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_ACCESS: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_BIT_SELECT_3: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_BIT_SELECT_4: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_BIT_SELECT_4_BYTE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_BRANCH_ABSOLUTE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_CALL_ACCESS: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_DMAOFFSET: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_DO_ABSOLUTE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_DSP_6: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_DSP_PRESHIFT: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_EDSOFFSET: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_EDSPAGE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_FILE_REG: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_FILE_REG_BYTE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_FILE_REG_WORD: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_FILE_REG_WORD_WITH_DST: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_FRAME_SIZE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_HANDLE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_L_ACCESS: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_L_PSVPTR: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_NONE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_PADDR: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_PBYTE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_PCREL_ACCESS: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_PCREL_BRANCH: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_PCREL_DO: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_PGM_ADDR_LSB: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_PGM_ADDR_MSB: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_PSVOFFSET: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_PSVPAGE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_PSVPTR: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_PWORD: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_PWRSAV_MODE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_P_ACCESS: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_P_DMAOFFSET: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_P_EDSOFFSET: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_P_EDSPAGE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_P_HANDLE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_P_PADDR: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_P_PSVOFFSET: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_P_PSVPAGE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_P_PSVPTR: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_P_TBLOFFSET: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_P_TBLPAGE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_SIGNED_10_BYTE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_TBLOFFSET: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_TBLPAGE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_UNSIGNED_10: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_UNSIGNED_14: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_UNSIGNED_4: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_UNSIGNED_5: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_UNSIGNED_8: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_WORD: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_WORD_ACCESS: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_WORD_DMAOFFSET: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_WORD_EDSOFFSET: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_WORD_EDSPAGE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_WORD_HANDLE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_WORD_PSVOFFSET: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_WORD_PSVPAGE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_WORD_PSVPTR: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_WORD_TBLOFFSET: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType
    R_PIC30_WORD_TBLPAGE: ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.PIC30_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

