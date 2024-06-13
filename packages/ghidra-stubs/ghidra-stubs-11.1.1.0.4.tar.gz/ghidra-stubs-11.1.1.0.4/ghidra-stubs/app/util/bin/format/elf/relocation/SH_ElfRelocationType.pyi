from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class SH_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    R_SH_64: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_64_PCREL: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_ALIGN: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_CODE: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_COPY: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_COPY64: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_COUNT: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DATA: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR10S: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR10SL: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR10SQ: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR10SW: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR16S: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR32: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR4U: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR4UL: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR4UW: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR5U: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR6S: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR6U: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR8: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR8BP: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR8L: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR8S: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR8SW: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR8U: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR8UL: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR8UW: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR8W: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR8WPL: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR8WPN: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_DIR8WPZ: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_FUNCDESC: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_FUNCDESC_VALUE: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GLOB_DAT: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GLOB_DAT64: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GNU_VTENTRY: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GNU_VTINHERIT: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOT10BY4: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOT10BY8: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOT20: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOT32: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTFUNCDESC: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTFUNCDESC20: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTOFF: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTOFF20: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTOFFFUNCDESC: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTOFFFUNCDESC20: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTOFF_HI16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTOFF_LOW16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTOFF_MEDHI16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTOFF_MEDLOW16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTPC: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTPC_HI16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTPC_LOW16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTPC_MEDHI16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTPC_MEDLOW16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTPLT10BY4: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTPLT10BY8: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTPLT32: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTPLT_HI16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTPLT_LOW16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTPLT_MEDHI16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOTPLT_MEDLOW16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOT_HI16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOT_LOW16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOT_MEDHI16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_GOT_MEDLOW16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_IMMS16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_IMMU16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_IMM_HI16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_IMM_HI16_PCREL: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_IMM_LOW16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_IMM_LOW16_PCREL: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_IMM_MEDHI16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_IMM_MEDHI16_PCREL: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_IMM_MEDLOW16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_IMM_MEDLOW16_PCREL: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_IND12W: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_JMP_SLOT: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_JMP_SLOT64: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_LABEL: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_LOOP_END: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_LOOP_START: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_NONE: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_PLT32: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_PLT_HI16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_PLT_LOW16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_PLT_MEDHI16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_PLT_MEDLOW16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_PSHA: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_PSHL: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_PT_16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_REL32: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_RELATIVE: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_RELATIVE64: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_SHMEDIA_CODE: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_SWITCH16: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_SWITCH32: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_SWITCH8: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_TLS_DTPMOD32: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_TLS_DTPOFF32: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_TLS_GD_32: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_TLS_IE_32: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_TLS_LDO_32: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_TLS_LD_32: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_TLS_LE_32: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_TLS_TPOFF32: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType
    R_SH_USES: ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.SH_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

