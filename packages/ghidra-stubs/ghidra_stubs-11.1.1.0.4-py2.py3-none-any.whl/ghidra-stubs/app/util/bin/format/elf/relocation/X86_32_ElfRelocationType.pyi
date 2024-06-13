from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class X86_32_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    R_386_32: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_32PLT: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_COPY: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_GLOB_DAT: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_GNU_VTENTRY: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_GNU_VTINHERIT: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_GOT32: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_GOT32X: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_GOTOFF: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_GOTPC: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_IRELATIVE: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_JMP_SLOT: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_NONE: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_PC32: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_PLT32: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_RELATIVE: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_DESC: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_DESC_CALL: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_DTPMOD32: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_DTPOFF32: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_GD: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_GD_32: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_GD_CALL: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_GD_POP: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_GD_PUSH: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_GOTDESC: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_GOTIE: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_IE: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_IE_32: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_LDM: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_LDM_32: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_LDM_CALL: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_LDM_POP: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_LDM_PUSH: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_LDO_32: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_LE: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_LE_32: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_TPOFF: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_TLS_TPOFF32: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType
    R_386_USED_BY_INTEL_200: ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.X86_32_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

