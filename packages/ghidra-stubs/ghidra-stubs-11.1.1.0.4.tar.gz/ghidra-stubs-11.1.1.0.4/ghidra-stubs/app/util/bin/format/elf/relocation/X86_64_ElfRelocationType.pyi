from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class X86_64_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    R_X86_64_16: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_32: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_32S: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_64: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_8: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_CODE_4_GOTPC32_TLSDESC: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_CODE_4_GOTPCRELX: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_CODE_4_GOTTPOFF: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_CODE_5_GOTPC32_TLSDESC: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_CODE_5_GOTPCRELX: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_CODE_5_GOTTPOFF: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_CODE_6_GOTPC32_TLSDESC: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_CODE_6_GOTPCRELX: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_CODE_6_GOTTPOFF: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_COPY: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_DTPMOD64: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_DTPOFF32: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_DTPOFF64: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_GLOB_DAT: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_GNU_VTENTRY: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_GNU_VTINHERIT: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_GOT32: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_GOT64: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_GOTOFF64: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_GOTPC32: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_GOTPC32_TLSDESC: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_GOTPC64: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_GOTPCREL: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_GOTPCREL64: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_GOTPCRELX: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_GOTPLT64: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_GOTTPOFF: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_IRELATIVE: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_JUMP_SLOT: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_NONE: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_PC16: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_PC32: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_PC32_BND: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_PC64: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_PC8: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_PLT32: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_PLT32_BND: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_PLTOFF64: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_RELATIVE: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_RELATIVE64: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_REX_GOTPCRELX: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_SIZE32: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_SIZE64: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_TLSDESC: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_TLSDESC_CALL: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_TLSGD: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_TLSLD: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_TPOFF32: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType
    R_X86_64_TPOFF64: ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.X86_64_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

