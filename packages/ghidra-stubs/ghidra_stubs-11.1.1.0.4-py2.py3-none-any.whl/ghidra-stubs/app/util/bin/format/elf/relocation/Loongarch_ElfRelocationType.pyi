from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class Loongarch_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    R_LARCH_32: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_32_PCREL: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_64: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_64_PCREL: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_ABS64_HI12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_ABS64_LO20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_ABS_HI20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_ABS_LO12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_ADD16: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_ADD24: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_ADD32: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_ADD6: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_ADD64: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_ADD8: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_ADD_ULEB128: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_ALIGN: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_B16: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_B21: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_B26: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_CALL32: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_CFA: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_COPY: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_DELETE: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_GNU_VTENTRY: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_GNU_VTINHERIT: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_GOT64_HI12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_GOT64_LO20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_GOT64_PC_HI12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_GOT64_PC_LO20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_GOT_HI20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_GOT_LO12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_GOT_PC_HI20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_GOT_PC_LO12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_IRELATIVE: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_JUMP_SLOT: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_MARK_LA: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_MARK_PCREL: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_NONE: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_PCALA64_HI12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_PCALA64_LO20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_PCALA_HI20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_PCALA_LO12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_PCREL20_S2: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_RELATIVE: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_RELAX: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_ADD: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_AND: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_ASSERT: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_IF_ELSE: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_NOT: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_POP_32_S_0_10_10_16_S2: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_POP_32_S_0_5_10_16_S2: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_POP_32_S_10_12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_POP_32_S_10_16: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_POP_32_S_10_16_S2: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_POP_32_S_10_5: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_POP_32_S_5_20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_POP_32_U: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_POP_32_U_10_12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_PUSH_ABSOLUTE: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_PUSH_DUP: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_PUSH_GPREL: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_PUSH_PCREL: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_PUSH_PLT_PCREL: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_PUSH_TLS_GD: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_PUSH_TLS_GOT: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_PUSH_TLS_TPREL: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_SL: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_SR: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SOP_SUB: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SUB16: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SUB24: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SUB32: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SUB6: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SUB64: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SUB8: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_SUB_ULEB128: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_DESC32: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_DESC64: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_DESC64_HI12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_DESC64_LO20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_DESC64_PC_HI12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_DESC64_PC_LO20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_DESC_CALL: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_DESC_HI20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_DESC_LD: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_DESC_LO12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_DESC_PC_HI20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_DESC_PC_LO12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_DTPMOD32: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_DTPMOD64: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_DTPREL32: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_DTPREL64: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_GD_HI20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_GD_PC_HI20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_IE64_HI12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_IE64_LO20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_IE64_PC_HI12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_IE64_PC_LO20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_IE_HI20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_IE_LO12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_IE_PC_HI20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_IE_PC_LO12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_LD_HI20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_LD_PC_HI20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_LE64_HI12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_LE64_LO20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_LE_HI20: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_LE_LO12: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_TLS_DESC_PCREL20_S2: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_TLS_GD_PCREL20_S2: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_TLS_LD_PCREL20_S2: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_TLS_LE_ADD_R: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_TLS_LE_HI20_R: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_TLS_LE_LO12_R: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_TPREL32: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType
    R_LARCH_TLS_TPREL64: ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.Loongarch_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

