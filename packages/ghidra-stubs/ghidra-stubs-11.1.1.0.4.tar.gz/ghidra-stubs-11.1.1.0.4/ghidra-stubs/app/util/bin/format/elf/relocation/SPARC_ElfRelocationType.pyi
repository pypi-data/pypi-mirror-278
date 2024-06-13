from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class SPARC_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    R_SPARC_10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_11: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_13: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_16: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_32: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_5: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_6: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_64: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_7: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_8: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_COPY: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_DISP16: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_DISP32: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_DISP64: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_DISP8: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_GLOB_DAT: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_GNU_VTENTRY: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_GNU_VTIHERIT: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_GOT10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_GOT13: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_GOT22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_GOTDATA_HIX22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_GOTDATA_LOX10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_GOTDATA_OP: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_GOTDATA_OP_HIX22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_GOTDATA_OP_LOX10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_H34: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_H44: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_HH22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_HI22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_HIPLT22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_HIX22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_HM10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_IRELATIVE: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_JMP_IREL: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_JMP_SLOT: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_L44: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_LM22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_LO10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_LOPLT10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_LOX10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_M44: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_NONE: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_OLO10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_PC10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_PC22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_PCPLT10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_PCPLT22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_PCPLT32: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_PC_H22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_PC_HM10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_PC_LM22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_PLT32: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_PLT64: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_REGISTER: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_RELATIVE: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_REV32: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_SIZE32: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_SIZE64: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_DTPMOD32: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_DTPMOD64: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_DTPOFF32: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_DTPOFF64: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_GD_ADD: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_GD_CALL: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_GD_HI22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_GD_LO10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_IE_: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_IE_ADD: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_IE_HI22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_IE_LDX: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_IE_LO10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_LDM_ADD: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_LDM_CALL: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_LDM_HI22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_LDM_LO10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_LDO_DD: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_LDO_HIX22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_LDO_LO10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_LE_HIX22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_LE_LOX10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_TPOFF32: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_TLS_TPOFF64: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_UA16: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_UA32: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_UA64: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_UNUSED_42: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_WDISP10: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_WDISP16: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_WDISP19: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_WDISP22: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_WDISP30: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType
    R_SPARC_WPLT30: ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.SPARC_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

