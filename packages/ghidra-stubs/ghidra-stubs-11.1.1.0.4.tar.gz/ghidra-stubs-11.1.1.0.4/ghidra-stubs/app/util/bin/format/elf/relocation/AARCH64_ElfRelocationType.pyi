from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class AARCH64_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    R_AARCH64_ABS16: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_ABS32: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_ABS64: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_ADD_ABS_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_ADR_GOT_PAGE: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_ADR_PREL_LO21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_ADR_PREL_PG_HI21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_ADR_PREL_PG_HI21_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_CALL26: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_CONDBR19: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_COPY: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_GLOB_DAT: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_GOTREL32: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_GOTREL64: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_GOT_LD_PREL19: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_IRELATIVE: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_JUMP26: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_JUMP_SLOT: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_LD64_GOTOFF_LO15: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_LD64_GOTPAGE_LO15: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_LD64_GOT_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_LDST128_ABS_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_LDST16_ABS_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_LDST32_ABS_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_LDST64_ABS_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_LDST8_ABS_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_LD_PREL_LO19: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_GOTOFF_G0: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_GOTOFF_G0_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_GOTOFF_G1: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_GOTOFF_G1_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_GOTOFF_G2: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_GOTOFF_G2_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_GOTOFF_G3: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_PREL_G0: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_PREL_G0_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_PREL_G1: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_PREL_G1_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_PREL_G2: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_PREL_G2_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_PREL_G3: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_SABS_G0: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_SABS_G1: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_SABS_G2: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_UABS_G0: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_UABS_G0_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_UABS_G1: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_UABS_G1_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_UABS_G2: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_UABS_G2_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_MOVW_UABS_G3: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_NONE: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_NULL: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_ABS16: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_ABS32: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_ADD_ABS_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_ADR_GOT_PAGE: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_ADR_PREL_LO21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_ADR_PREL_PG_HI21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_CALL26: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_CONDBR19: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_COPY: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_GLOB_DAT: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_GOT_LD_PREL19: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_IRELATIVE: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_JUMP26: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_JUMP_SLOT: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_LD32_GOTPAGE_LO14: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_LD32_GOT_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_LDST128_ABS_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_LDST16_ABS_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_LDST32_ABS_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_LDST64_ABS_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_LDST8_ABS_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_LD_PREL_LO19: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_MOVW_SABS_G0: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_MOVW_UABS_G0: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_MOVW_UABS_G0_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_MOVW_UABS_G1: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_PREL16: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_PREL32: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_RELATIVE: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSDESC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSDESC_ADD_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSDESC_ADR_PAGE21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSDESC_ADR_PREL21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSDESC_CALL: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSDESC_LD32_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSDESC_LD_PREL19: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSGD_ADD_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSGD_ADR_PAGE21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSGD_ADR_PREL21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSIE_ADR_GOTTPREL_PAGE21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSIE_LD32_GOTTPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSIE_LD_GOTTPREL_PREL19: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLD_ADD_DTPREL_HI12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLD_ADD_DTPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLD_ADD_DTPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLD_ADD_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLD_ADR_PAGE21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLD_ADR_PREL21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLD_MOVW_DTPREL_G0: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLD_MOVW_DTPREL_G0_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLD_MOVW_DTPREL_G1: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLE_ADD_TPREL_HI12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLE_ADD_TPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLE_ADD_TPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLE_LDST16_TPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLE_LDST16_TPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLE_LDST32_TPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLE_LDST32_TPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLE_LDST64_TPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLE_LDST64_TPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLE_LDST8_TPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLE_LDST8_TPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLE_MOVW_TPREL_G0: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLE_MOVW_TPREL_G0_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLSLE_MOVW_TPREL_G1: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLS_DTPMOD: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLS_DTPREL: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TLS_TPREL: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_P32_TSTBR14: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_PREL16: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_PREL32: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_PREL64: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_RELATIVE: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSDESC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSDESC_ADD: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSDESC_ADD_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSDESC_ADR_PAGE21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSDESC_ADR_PREL21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSDESC_CALL: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSDESC_LD64_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSDESC_LDR: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSDESC_LD_PREL19: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSDESC_OFF_G0_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSDESC_OFF_G1: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSGD_ADD_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSGD_ADR_PAGE21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSGD_ADR_PREL21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSGD_MOVW_G0_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSGD_MOVW_G1: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSIE_ADR_GOTTPREL_PAGE21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSIE_LD64_GOTTPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSIE_LD_GOTTPREL_PREL19: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSIE_MOVW_GOTTPREL_G0_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSIE_MOVW_GOTTPREL_G1: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_ADD_DTPREL_HI12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_ADD_DTPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_ADD_DTPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_ADD_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_ADR_PAGE21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_ADR_PREL21: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_LDST128_DTPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_LDST128_DTPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_LDST16_DTPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_LDST16_DTPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_LDST32_DTPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_LDST32_DTPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_LDST64_DTPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_LDST64_DTPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_LDST8_DTPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_LDST8_DTPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_LD_PREL19: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_MOVW_DTPREL_G0: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_MOVW_DTPREL_G0_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_MOVW_DTPREL_G1: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_MOVW_DTPREL_G1_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_MOVW_DTPREL_G2: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_MOVW_G0_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLD_MOVW_G1: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_ADD_TPREL_HI12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_ADD_TPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_ADD_TPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_LDST128_TPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_LDST128_TPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_LDST16_TPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_LDST16_TPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_LDST32_TPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_LDST32_TPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_LDST64_TPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_LDST64_TPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_LDST8_TPREL_LO12: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_LDST8_TPREL_LO12_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_MOVW_TPREL_G0: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_MOVW_TPREL_G0_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_MOVW_TPREL_G1: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_MOVW_TPREL_G1_NC: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLSLE_MOVW_TPREL_G2: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLS_DTPMOD: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLS_DTPMOD64: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLS_DTPREL: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLS_DTPREL64: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLS_TPREL: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TLS_TPREL64: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType
    R_AARCH64_TSTBR14: ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.AARCH64_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

