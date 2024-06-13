from typing import List
from typing import overload
import ghidra.app.util.bin.format.pdb2.pdbreader
import java.lang
import java.util


class ImageFileMachine(java.lang.Enum):
    ALPHA: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    ALPHA64: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    AM33: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    AMD64: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    ARM: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    ARM64: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    ARMNT: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    AXP64: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    CEE: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    CEF: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    EBC: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    I386: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    I860: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    IA64: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    M32R: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    M68K: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    MIPS16: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    MIPSFPU: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    MIPSFPU16: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    POWERPC: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    POWERPCBE: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    POWERPCFP: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    R10000: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    R3000: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    R4000: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    SH3: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    SH3DSP: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    SH3E: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    SH4: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    SH5: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    TARGET_HOST: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    THUMB: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    TRICORE: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    UNKNOWN: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine
    WCEMIPSV2: ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def fromValue(__a0: int) -> ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def getProcessor(self) -> ghidra.app.util.bin.format.pdb2.pdbreader.Processor: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.pdb2.pdbreader.ImageFileMachine]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def processor(self) -> ghidra.app.util.bin.format.pdb2.pdbreader.Processor: ...