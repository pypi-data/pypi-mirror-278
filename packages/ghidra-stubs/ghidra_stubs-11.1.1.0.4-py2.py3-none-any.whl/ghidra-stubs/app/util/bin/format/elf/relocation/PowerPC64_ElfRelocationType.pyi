from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class PowerPC64_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    R_PPC64_ADDR14: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR14_BRNTAKEN: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR14_BRTAKEN: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR16: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR16_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR16_HIGH: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR16_HIGHA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR16_HIGHER: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR16_HIGHER34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR16_HIGHERA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR16_HIGHERA34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR16_HIGHEST: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR16_HIGHEST34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR16_HIGHESTA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR16_HIGHESTA34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR16_LO_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR24: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR30: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR32: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR64: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ADDR64_LOCAL: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_COPY: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_D28: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_D34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_D34_HA30: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_D34_HI30: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_D34_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_DTPMOD64: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_DTPREL16: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_DTPREL16_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_DTPREL16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_DTPREL16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_DTPREL16_HIGH: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_DTPREL16_HIGHA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_DTPREL16_HIGHER: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_DTPREL16_HIGHERA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_DTPREL16_HIGHEST: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_DTPREL16_HIGHESTA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_DTPREL16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_DTPREL16_LO_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_DTPREL34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_DTPREL64: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_ENTRY: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GLOB_DAT: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT16: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT16_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT16_LO_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_DTPREL16_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_DTPREL16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_DTPREL16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_DTPREL16_LO_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_DTPREL_PCREL34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_PCREL34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_TLSGD16: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_TLSGD16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_TLSGD16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_TLSGD16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_TLSGD_PCREL34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_TLSLD16: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_TLSLD16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_TLSLD16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_TLSLD16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_TLSLD_PCREL34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_TPREL16_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_TPREL16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_TPREL16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_TPREL16_LO_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_GOT_TPREL_PCREL34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_IRELATIVE: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_JMP_IREL: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_JMP_SLOT: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_NONE: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PCREL28: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PCREL34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PCREL_OPT: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLT16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLT16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLT16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLT16_LO_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLT32: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLT64: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLTCALL: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLTCALL_NOTOC: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLTGOT16: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLTGOT16_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLTGOT16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLTGOT16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLTGOT16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLTGOT16_LO_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLTREL32: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLTREL64: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLTSEQ: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLTSEQ_NOTOC: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLT_PCREL34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_PLT_PCREL34_NOTOC: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL14: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL14_BRNTAKEN: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL14_BRTAKEN: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL16: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL16DX_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL16_HIGH: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL16_HIGHA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL16_HIGHER: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL16_HIGHER34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL16_HIGHERA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL16_HIGHERA34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL16_HIGHEST: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL16_HIGHEST34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL16_HIGHESTA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL16_HIGHESTA34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL24: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL24_NOTOC: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL24_P9NOTOC: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL32: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_REL64: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_RELATIVE: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_SECTOFF: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_SECTOFF_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_SECTOFF_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_SECTOFF_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_SECTOFF_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_SECTOFF_LO_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TLS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TLSGD: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TLSLD: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TOC: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TOC16: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TOC16_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TOC16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TOC16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TOC16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TOC16_LO_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TOCSAVE: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TPREL16: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TPREL16_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TPREL16_HA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TPREL16_HI: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TPREL16_HIGH: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TPREL16_HIGHA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TPREL16_HIGHER: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TPREL16_HIGHERA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TPREL16_HIGHEST: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TPREL16_HIGHESTA: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TPREL16_LO: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TPREL16_LO_DS: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TPREL34: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_TPREL64: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_UADDR16: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_UADDR32: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_UADDR64: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_VTENTRY: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType
    R_PPC64_VTINHERIT: ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.PowerPC64_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

