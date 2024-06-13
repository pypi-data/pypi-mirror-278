from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class RISCV_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    R_RISCV_32: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_32_PCREL: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_64: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_ADD16: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_ADD32: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_ADD64: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_ADD8: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_ALIGN: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_BRANCH: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_CALL: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_CALL_PLT: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_COPY: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_GNU_VTENTRY: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_GNU_VTINHERIT: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_GOT_HI20: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_GPREL_I: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_GPREL_S: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_HI20: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_IRELATIVE: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_JAL: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_JUMP_SLOT: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_LO12_I: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_LO12_S: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_NONE: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_PCREL_HI20: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_PCREL_LO12_I: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_PCREL_LO12_S: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_RELATIVE: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_RELAX: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_RVC_BRANCH: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_RVC_JUMP: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_RVC_LUI: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_SET16: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_SET32: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_SET6: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_SET8: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_SET_ULEB128: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_SUB16: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_SUB32: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_SUB6: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_SUB64: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_SUB8: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_SUB_ULEB128: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TLSDESC: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TLSDESC_ADD_LO12: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TLSDESC_CALL: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TLSDESC_HI20: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TLSDESC_LOAD_LO12: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TLS_DTPMOD32: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TLS_DTPMOD64: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TLS_DTPREL32: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TLS_DTPREL64: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TLS_GD_HI20: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TLS_GOT_HI20: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TLS_TPREL32: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TLS_TPREL64: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TPREL_ADD: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TPREL_HI20: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TPREL_I: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TPREL_LO12_I: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TPREL_LO12_S: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType
    R_RISCV_TPREL_S: ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.RISCV_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

