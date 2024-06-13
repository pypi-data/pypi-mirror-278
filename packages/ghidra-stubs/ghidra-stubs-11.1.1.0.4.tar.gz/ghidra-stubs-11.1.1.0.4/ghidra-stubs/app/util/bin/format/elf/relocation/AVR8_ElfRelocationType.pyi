from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class AVR8_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    R_AVR_13_PCREL: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_16: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_16_PM: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_32: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_32_PCREL: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_6: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_6_ADIW: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_7_PCREL: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_8: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_8_HI8: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_8_HLO8: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_8_LO8: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_CALL: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_DIFF16: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_DIFF32: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_DIFF8: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_HH8_LDI: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_HH8_LDI_NEG: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_HH8_LDI_PM: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_HH8_LDI_PM_NEG: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_HI8_LDI: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_HI8_LDI_GS: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_HI8_LDI_NEG: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_HI8_LDI_PM: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_HI8_LDI_PM_NEG: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_LDI: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_LDS_STS_16: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_LO8_LDI: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_LO8_LDI_GS: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_LO8_LDI_NEG: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_LO8_LDI_PM: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_LO8_LDI_PM_NEG: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_MS8_LDI: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_MS8_LDI_NEG: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_NONE: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_PORT5: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType
    R_AVR_PORT6: ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.AVR8_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

