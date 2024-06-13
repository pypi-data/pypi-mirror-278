from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class MIPS_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    R_MICROMIPS_26_S1: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_CALL16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_CALL_HI16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_CALL_LO16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_GOT16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_GOT_DISP: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_GOT_HI16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_GOT_LO16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_GOT_OFST: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_GOT_PAGE: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_GPREL16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_GPREL7_S2: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_HI: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_HI0_LO16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_HI16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_HIGHER: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_HIGHEST: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_JALR: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_LITERAL: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_LO: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_LO16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_PC10_S1: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_PC16_S1: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_PC23_S2: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_PC7_S1: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_SCN_DISP: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_SUB: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_TLS_DTPREL_HI16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_TLS_DTPREL_LO16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_TLS_GD: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_TLS_GOTTPREL: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_TLS_LDM: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_TLS_TPREL_HI16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MICROMIPS_TLS_TPREL_LO16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS16_26: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS16_CALL16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS16_GOT16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS16_GPREL: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS16_HI: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS16_HI16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS16_LO: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS16_LO16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS16_PC16_S1: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS16_TLS_DTPREL_HI16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS16_TLS_DTPREL_LO16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS16_TLS_GD: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS16_TLS_GOTTPREL: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS16_TLS_LDM: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS16_TLS_TPREL_HI16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS16_TLS_TPREL_LO16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_26: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_32: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_64: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_ADD_IMMEDIATE: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_CALL16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_CALL_HI16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_CALL_LO16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_COPY: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_DELETE: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_EH: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_GLOB_DAT: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_GNU_REL16_S2: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_GNU_VTENTRY: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_GNU_VTINHERIT: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_GOT16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_GOT_DISP: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_GOT_HI16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_GOT_LO16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_GOT_OFST: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_GOT_PAGE: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_GPREL16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_GPREL32: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_HI16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_HIGHER: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_HIGHEST: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_INSERT_A: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_INSERT_B: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_JALR: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_JUMP_SLOT: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_LITERAL: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_LO16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_NONE: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_PC16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_PC18_S3: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_PC19_S2: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_PC21_S2: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_PC26_S2: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_PC32: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_PCHI16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_PCLO16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_PJUMP: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_REL16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_REL32: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_RELGOT: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_SCN_DISP: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_SHIFT5: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_SHIFT6: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_SUB: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_TLS_DTPMOD32: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_TLS_DTPMOD64: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_TLS_DTPREL32: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_TLS_DTPREL64: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_TLS_DTPREL_HI16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_TLS_DTPREL_LO16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_TLS_GD: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_TLS_GOTTPREL: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_TLS_LDM: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_TLS_TPREL32: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_TLS_TPREL64: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_TLS_TPREL_HI16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_TLS_TPREL_LO16: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_UNUSED1: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_UNUSED2: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType
    R_MIPS_UNUSED3: ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.MIPS_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

