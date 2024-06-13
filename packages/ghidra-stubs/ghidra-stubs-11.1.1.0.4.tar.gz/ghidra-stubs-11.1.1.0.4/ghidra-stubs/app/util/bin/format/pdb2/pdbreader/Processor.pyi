from typing import List
from typing import overload
import ghidra.app.util.bin.format.pdb2.pdbreader
import java.lang
import java.util


class Processor(java.lang.Enum):
    ALPHA_21064: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    ALPHA_21164: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    ALPHA_21164A: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    ALPHA_21264: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    ALPHA_21364: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    AM33: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    ARM3: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    ARM4: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    ARM4T: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    ARM5: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    ARM5T: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    ARM6: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    ARM64: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    ARM7: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    ARMNT: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    ARM_WMMX: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    ARM_XMAC: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    CEE: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    D3D11_SHADER: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    EBC: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    I80286: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    I80386: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    I80486: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    I8080: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    I8086: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    IA64_2: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    IA64_IA64_1: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    M32R: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    M68000: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    M68010: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    M68020: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    M68030: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    M68040: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    MIPS16: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    MIPS32: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    MIPS64: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    MIPSI: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    MIPSII: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    MIPSIII: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    MIPSIV: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    MIPSV: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    MIPS_MIPSR4000: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    OMNI: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    PENTIUM: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    PENTIUMIII: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    PENTIUMPRO_PENTIUMII: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    PPC601: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    PPC603: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    PPC604: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    PPC620: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    PPCBE: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    PPCFP: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    SH3: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    SH3DSP: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    SH3E: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    SH4: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    SHMEDIA: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    THUMB: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    TRICORE: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    UNK1AB: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    UNK304: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    UNKNOWN: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    X64_AMD64: ghidra.app.util.bin.format.pdb2.pdbreader.Processor
    label: unicode







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def fromValue(__a0: int) -> ghidra.app.util.bin.format.pdb2.pdbreader.Processor: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def getValue(self) -> int: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.pdb2.pdbreader.Processor: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.pdb2.pdbreader.Processor]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def value(self) -> int: ...