from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class Xtensa_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    R_XTENSA_32: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_32_PCREL: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_ASM_EXPAND: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_ASM_SIMPLIFY: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_DIFF16: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_DIFF32: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_DIFF8: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_GLOB_DAT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_GNU_VTENTRY: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_GNU_VTINHERIT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_JMP_SLOT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_NDIFF16: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_NDIFF32: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_NDIFF8: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_NONE: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_OP0: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_OP1: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_OP2: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_PDIFF16: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_PDIFF32: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_PDIFF8: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_PLT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_RELATIVE: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_RTLD: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT0_ALT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT0_OP: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT10_ALT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT10_OP: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT11_ALT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT11_OP: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT12_ALT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT12_OP: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT13_ALT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT13_OP: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT14_ALT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT14_OP: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT1_ALT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT1_OP: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT2_ALT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT2_OP: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT3_ALT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT3_OP: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT4_ALT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT4_OP: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT5_ALT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT5_OP: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT6_ALT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT6_OP: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT7_ALT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT7_OP: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT8_ALT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT8_OP: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT9_ALT: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_SLOT9_OP: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_TLSDESC_ARG: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_TLSDESC_FN: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_TLS_ARG: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_TLS_CALL: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_TLS_DTPOFF: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_TLS_FUNC: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType
    R_XTENSA_TLS_TPOFF: ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.Xtensa_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

