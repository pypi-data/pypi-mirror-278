from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf.relocation
import java.lang
import java.util


class Tricore_ElfRelocationType(java.lang.Enum, ghidra.app.util.bin.format.elf.relocation.ElfRelocationType):
    EF_TRICORE_PCP2: int = 33554432
    EF_TRICORE_V1_1: int = -2147483648
    EF_TRICORE_V1_2: int = 1073741824
    EF_TRICORE_V1_3: int = 536870912
    R_TRICORE_10A8: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_10A9: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_10LI: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_10OFF: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_10SM: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_15REL: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_16A8: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_16A9: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_16ABS: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_16BIT: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_16LI: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_16OFF: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_16SM: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_16SM2: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_18ABS: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_24ABS: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_24REL: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_2OFF: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_32ABS: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_32REL: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_3POS: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_42OFF: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_42OFF2: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_42OFF4: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_4CONST: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_4OFF: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_4OFF2: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_4OFF4: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_4POS: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_4REL: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_4REL2: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_5POS: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_5POS2: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_5POS3: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_5REL: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_8ABS: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_8CONST2: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_BITPOS: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_BRCC: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_BRCZ: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_BRNN: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_COPY: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GLOB_DAT: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOT: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOT2: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOTCPUP: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOTHI: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOTLO: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOTLO2: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOTOFF: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOTOFF2: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOTOFFHI: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOTOFFLO: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOTOFFLO2: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOTOFFUP: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOTPC: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOTPC2: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOTPCHI: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOTPCLO: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOTPCLO2: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_GOTUP: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_HI: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_JMP_SLOT: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_LO: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_LO2: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_NONE: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_PCPHI: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_PCPLO: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_PCPOFF: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_PCPPAGE: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_PCPTEXT: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_PCREL16: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_PCREL8: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_PLT: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_RELATIVE: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_RRN: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_SBREG_D: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_SBREG_S1: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_SBREG_S2: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_VTENTRY: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    R_TRICORE_VTINHERIT: ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType
    SHF_TRICORE_ABS: int = 1024
    SHF_TRICORE_NOREAD: int = 2048







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
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.elf.relocation.Tricore_ElfRelocationType]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

