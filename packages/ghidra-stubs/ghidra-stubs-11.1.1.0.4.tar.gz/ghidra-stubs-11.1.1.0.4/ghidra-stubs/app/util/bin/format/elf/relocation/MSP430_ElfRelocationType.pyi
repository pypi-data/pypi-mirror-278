from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class MSP430_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    R_MSP430_10_PCREL: ghidra.app.util.bin.format.elf.relocation.MSP430_ElfRelocationType
    R_MSP430_16: ghidra.app.util.bin.format.elf.relocation.MSP430_ElfRelocationType
    R_MSP430_16_BYTE: ghidra.app.util.bin.format.elf.relocation.MSP430_ElfRelocationType
    R_MSP430_16_PCREL: ghidra.app.util.bin.format.elf.relocation.MSP430_ElfRelocationType
    R_MSP430_16_PCREL_BYTE: ghidra.app.util.bin.format.elf.relocation.MSP430_ElfRelocationType
    R_MSP430_2X_PCREL: ghidra.app.util.bin.format.elf.relocation.MSP430_ElfRelocationType
    R_MSP430_32: ghidra.app.util.bin.format.elf.relocation.MSP430_ElfRelocationType
    R_MSP430_8: ghidra.app.util.bin.format.elf.relocation.MSP430_ElfRelocationType
    R_MSP430_NONE: ghidra.app.util.bin.format.elf.relocation.MSP430_ElfRelocationType
    R_MSP430_RL_PCREL: ghidra.app.util.bin.format.elf.relocation.MSP430_ElfRelocationType
    R_MSP430_SET_ULEB128: ghidra.app.util.bin.format.elf.relocation.MSP430_ElfRelocationType
    R_MSP430_SUB_ULEB128: ghidra.app.util.bin.format.elf.relocation.MSP430_ElfRelocationType
    R_MSP430_SYM_DIFF: ghidra.app.util.bin.format.elf.relocation.MSP430_ElfRelocationType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.MSP430_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.MSP430_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

