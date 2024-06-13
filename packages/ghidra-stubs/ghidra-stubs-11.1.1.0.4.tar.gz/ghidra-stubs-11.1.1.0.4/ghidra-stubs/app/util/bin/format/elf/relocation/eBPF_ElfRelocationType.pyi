from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class eBPF_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    R_BPF_64_32: ghidra.app.util.bin.format.elf.relocation.eBPF_ElfRelocationType
    R_BPF_64_64: ghidra.app.util.bin.format.elf.relocation.eBPF_ElfRelocationType
    R_BPF_64_ABS32: ghidra.app.util.bin.format.elf.relocation.eBPF_ElfRelocationType
    R_BPF_64_ABS64: ghidra.app.util.bin.format.elf.relocation.eBPF_ElfRelocationType
    R_BPF_64_NODYLD32: ghidra.app.util.bin.format.elf.relocation.eBPF_ElfRelocationType
    R_BPF_GNU_64_16: ghidra.app.util.bin.format.elf.relocation.eBPF_ElfRelocationType
    R_BPF_NONE: ghidra.app.util.bin.format.elf.relocation.eBPF_ElfRelocationType







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.eBPF_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.eBPF_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

