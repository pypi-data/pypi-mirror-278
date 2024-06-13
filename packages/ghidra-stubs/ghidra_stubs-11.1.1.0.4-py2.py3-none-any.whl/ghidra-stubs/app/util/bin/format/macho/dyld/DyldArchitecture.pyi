from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.macho.dyld
import ghidra.program.model.lang
import java.lang


class DyldArchitecture(object):
    ARCHITECTURES: List[ghidra.app.util.bin.format.macho.dyld.DyldArchitecture]
    ARM64_32: ghidra.app.util.bin.format.macho.dyld.DyldArchitecture
    ARMV6: ghidra.app.util.bin.format.macho.dyld.DyldArchitecture
    ARMV7: ghidra.app.util.bin.format.macho.dyld.DyldArchitecture
    ARMV7F: ghidra.app.util.bin.format.macho.dyld.DyldArchitecture
    ARMV7K: ghidra.app.util.bin.format.macho.dyld.DyldArchitecture
    ARMV7S: ghidra.app.util.bin.format.macho.dyld.DyldArchitecture
    ARMV8A: ghidra.app.util.bin.format.macho.dyld.DyldArchitecture
    ARMV8Ae: ghidra.app.util.bin.format.macho.dyld.DyldArchitecture
    DYLD_V1_SIGNATURE_LEN: int = 16
    DYLD_V1_SIGNATURE_PREFIX: unicode = u'dyld_v1'
    POWERPC: ghidra.app.util.bin.format.macho.dyld.DyldArchitecture
    X86: ghidra.app.util.bin.format.macho.dyld.DyldArchitecture
    X86_64: ghidra.app.util.bin.format.macho.dyld.DyldArchitecture
    X86_64h: ghidra.app.util.bin.format.macho.dyld.DyldArchitecture







    def equals(self, __a0: object) -> bool: ...

    @overload
    @staticmethod
    def getArchitecture(signature: unicode) -> ghidra.app.util.bin.format.macho.dyld.DyldArchitecture:
        """
        Returns the architecture object with the given signature.
         Returns NULL if one does not exist.
        @param signature the signature string
        @return the architecture object with the given signature or NULL
        """
        ...

    @overload
    @staticmethod
    def getArchitecture(provider: ghidra.app.util.bin.ByteProvider) -> ghidra.app.util.bin.format.macho.dyld.DyldArchitecture: ...

    def getClass(self) -> java.lang.Class: ...

    def getCpuSubType(self) -> int: ...

    def getCpuType(self) -> int: ...

    def getEndianness(self) -> ghidra.program.model.lang.Endian: ...

    def getLanguageCompilerSpecPair(self, languageService: ghidra.program.model.lang.LanguageService) -> ghidra.program.model.lang.LanguageCompilerSpecPair: ...

    def getProcessor(self) -> unicode: ...

    def getSignature(self) -> unicode: ...

    def hashCode(self) -> int: ...

    def is64bit(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def 64bit(self) -> bool: ...

    @property
    def cpuSubType(self) -> int: ...

    @property
    def cpuType(self) -> int: ...

    @property
    def endianness(self) -> ghidra.program.model.lang.Endian: ...

    @property
    def processor(self) -> unicode: ...

    @property
    def signature(self) -> unicode: ...