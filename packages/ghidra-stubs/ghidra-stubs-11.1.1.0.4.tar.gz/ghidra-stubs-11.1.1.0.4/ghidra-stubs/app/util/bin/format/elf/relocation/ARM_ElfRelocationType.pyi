from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class ARM_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    R_ARM_ABS12: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ABS16: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ABS32: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ABS32_NOI: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ABS_8: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ALU_PCREL_15_8: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ALU_PCREL_23_15: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ALU_PCREL_7_0: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ALU_PC_G0: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ALU_PC_G0_NC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ALU_PC_G1: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ALU_PC_G1_NC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ALU_PC_G2: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ALU_SBREL_19_12_NC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ALU_SBREL_27_20_CK: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ALU_SB_G0: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ALU_SB_G0_NC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ALU_SB_G1: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ALU_SB_G1_NC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ALU_SB_G2: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_BASE_ABS: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_BASE_PREL: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_BREL_ADJ: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_CALL: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_COPY: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_FUNCDESC_VALUE: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_FUNCESC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_GLOB_DAT: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_GNU_VTENTRY: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_GNU_VTINHERIT: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_GOTFUNCDEC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_GOTOFF12: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_GOTOFF32: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_GOTOFFFUNCDESC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_GOTRELAX: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_GOT_ABS: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_GOT_BREL: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_GOT_BREL12: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_GOT_PREL: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_IRELATIVE: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_JUMP24: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_JUMP_SLOT: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDC_PC_G0: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDC_PC_G1: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDC_PC_G2: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDC_SB_G0: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDC_SB_G1: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDC_SB_G2: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDRS_PC_G0: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDRS_PC_G1: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDRS_PC_G2: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDRS_SB_G0: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDRS_SB_G1: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDRS_SB_G2: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDR_PC_G0: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDR_PC_G1: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDR_PC_G2: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDR_SBREL_11_0_NC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDR_SB_G0: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDR_SB_G1: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_LDR_SB_G2: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_ME_TOO: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_MOVT_ABS: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_MOVT_BREL: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_MOVT_PREL: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_MOVW_ABS_NC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_MOVW_BREL: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_MOVW_BREL_NC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_MOVW_PREL_NC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_NONE: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PC24: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PLT32: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PLT32_ABS: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PREL31: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PRIVATE_0: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PRIVATE_1: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PRIVATE_10: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PRIVATE_11: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PRIVATE_12: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PRIVATE_13: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PRIVATE_14: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PRIVATE_15: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PRIVATE_2: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PRIVATE_3: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PRIVATE_4: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PRIVATE_5: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PRIVATE_6: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PRIVATE_7: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PRIVATE_8: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_PRIVATE_9: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_RABS32: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_RBASE: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_REL32: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_REL32_NOI: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_RELATIVE: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_RPC24: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_RREL32: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_RSBREL32: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_RXPC25: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_SBREL31: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_SBREL32: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TARGET1: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TARGET2: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_ABS5: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_ALU_ABS_G0_NC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_ALU_ABS_G1_NC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_ALU_ABS_G2_NC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_ALU_ABS_G3_NC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_ALU_PREL_11_0: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_BF12: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_BF16: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_BF18: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_CALL: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_JUMP11: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_JUMP19: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_JUMP24: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_JUMP6: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_JUMP8: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_MOVT_ABS: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_MOVT_BREL: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_MOVT_PREL: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_MOVW_ABS_NC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_MOVW_BREL: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_MOVW_BREL_NC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_MOVW_PREL_NC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_PC12: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_PC8: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_RPC22: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_SWI8: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_TLS_CALL: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_TLS_DESCSEQ16: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_TLS_DESCSEQ32: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_THM_XPC22: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_CALL: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_DESC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_DESCSEQ: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_DTPMOD32: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_DTPOFF32: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_GD32: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_GD32_FDPIC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_GOTDESC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_IE12GP: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_IE32: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_IE32_FDPIC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_LDM32: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_LDM32_FDPIC: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_LDO12: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_LDO32: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_LE12: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_LE32: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_TLS_TPOFF32: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_V4BX: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType
    R_ARM_XPC25: ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.ARM_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

