from typing import List
from typing import overload
import ghidra.framework
import java.lang
import java.util


class Platform(java.lang.Enum):
    CURRENT_PLATFORM: ghidra.framework.Platform
    FREEBSD_ARM_64: ghidra.framework.Platform
    FREEBSD_X86_64: ghidra.framework.Platform
    LINUX: ghidra.framework.Platform
    LINUX_64: ghidra.framework.Platform
    LINUX_ARM_64: ghidra.framework.Platform
    LINUX_UKNOWN: ghidra.framework.Platform
    LINUX_X86_32: ghidra.framework.Platform
    LINUX_X86_64: ghidra.framework.Platform
    MAC_ARM_64: ghidra.framework.Platform
    MAC_OSX_32: ghidra.framework.Platform
    MAC_OSX_64: ghidra.framework.Platform
    MAC_UNKNOWN: ghidra.framework.Platform
    MAC_X86_32: ghidra.framework.Platform
    MAC_X86_64: ghidra.framework.Platform
    UNSUPPORTED: ghidra.framework.Platform
    WIN_64: ghidra.framework.Platform
    WIN_UNKOWN: ghidra.framework.Platform
    WIN_X86_32: ghidra.framework.Platform
    WIN_X86_64: ghidra.framework.Platform







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getAdditionalLibraryPaths(self) -> List[object]: ...

    def getArchitecture(self) -> ghidra.framework.Architecture: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def getDirectoryName(self) -> unicode: ...

    def getExecutableExtension(self) -> unicode: ...

    def getLibraryExtension(self) -> unicode: ...

    def getOperatingSystem(self) -> ghidra.framework.OperatingSystem: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.framework.Platform: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.framework.Platform]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def additionalLibraryPaths(self) -> List[object]: ...

    @property
    def architecture(self) -> ghidra.framework.Architecture: ...

    @property
    def directoryName(self) -> unicode: ...

    @property
    def executableExtension(self) -> unicode: ...

    @property
    def libraryExtension(self) -> unicode: ...

    @property
    def operatingSystem(self) -> ghidra.framework.OperatingSystem: ...