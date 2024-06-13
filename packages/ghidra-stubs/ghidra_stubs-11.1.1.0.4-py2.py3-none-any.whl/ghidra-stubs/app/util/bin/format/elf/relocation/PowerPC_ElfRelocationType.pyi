from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class PowerPC_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    R_POWERPC_DTPMOD: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_DTPREL: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_DTPREL16: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_DTPREL16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_DTPREL16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_DTPREL16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GNU_VTENTRY: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GNU_VTINHERIT: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GOT_DTPREL16: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GOT_DTPREL16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GOT_DTPREL16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GOT_DTPREL16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GOT_TLSGD16: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GOT_TLSGD16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GOT_TLSGD16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GOT_TLSGD16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GOT_TLSLD16: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GOT_TLSLD16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GOT_TLSLD16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GOT_TLSLD16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GOT_TPREL16: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GOT_TPREL16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GOT_TPREL16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_GOT_TPREL16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_IRELATIVE: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_PLTCALL: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_PLTSEQ: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_REL16: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_REL16DX_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_REL16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_REL16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_REL16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_TLS: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_TPREL: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_TPREL16: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_TPREL16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_TPREL16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_POWERPC_TPREL16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_16DX_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_ADDR14: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_ADDR14_BRNTAKEN: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_ADDR14_BRTAKEN: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_ADDR16: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_ADDR16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_ADDR16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_ADDR16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_ADDR24: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_ADDR30: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_ADDR32: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_COPY: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_EMB_BIT_FLD: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_EMB_MRKREF: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_EMB_NADDR16: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_EMB_NADDR16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_EMB_NADDR16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_EMB_NADDR16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_EMB_NADDR32: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_EMB_RELSDA: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_EMB_RELSEC16: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_EMB_RELST_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_EMB_RELST_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_EMB_RELST_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_EMB_SDA21: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_EMB_SDA2I16: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_EMB_SDA2REL: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_EMB_SDAI16: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_GLOB_DAT: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_GOT16: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_GOT16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_GOT16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_GOT16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_JMP_SLOT: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_LOCAL24PC: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_NONE: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_PLT16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_PLT16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_PLT16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_PLT32: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_PLTREL24: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_PLTREL32: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_REL14: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_REL14_BRNTAKEN: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_REL14_BRTAKEN: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_REL24: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_REL32: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_RELATIVE: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_RELAX: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_RELAX_PLT: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_RELAX_PLTREL24: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_SDAREL16: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_SECTOFF: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_SECTOFF_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_SECTOFF_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_SECTOFF_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_TLSGD: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_TLSLD: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_TOC16: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_UADDR16: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_UADDR32: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_VLE_HA16A: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_VLE_HA16D: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_VLE_HI16A: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_VLE_HI16D: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_VLE_LO16A: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_VLE_LO16D: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_VLE_REL15: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_VLE_REL24: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_VLE_REL8: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_VLE_SDA21: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_VLE_SDA21_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_VLE_SDAREL_HA16A: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_VLE_SDAREL_HA16D: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_VLE_SDAREL_HI16A: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_VLE_SDAREL_HI16D: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_VLE_SDAREL_LO16A: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType
    R_PPC_VLE_SDAREL_LO16D: ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.PowerPC_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

