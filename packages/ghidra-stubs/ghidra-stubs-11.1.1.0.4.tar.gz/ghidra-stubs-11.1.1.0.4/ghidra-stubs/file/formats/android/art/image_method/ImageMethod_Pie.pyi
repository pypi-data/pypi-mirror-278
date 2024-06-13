from typing import List
from typing import overload
import ghidra.file.formats.android.art.image_method
import java.lang
import java.util


class ImageMethod_Pie(java.lang.Enum):
    kImageMethodsCount: ghidra.file.formats.android.art.image_method.ImageMethod_Pie
    kImtConflictMethod: ghidra.file.formats.android.art.image_method.ImageMethod_Pie
    kImtUnimplementedMethod: ghidra.file.formats.android.art.image_method.ImageMethod_Pie
    kResolutionMethod: ghidra.file.formats.android.art.image_method.ImageMethod_Pie
    kSaveAllCalleeSavesMethod: ghidra.file.formats.android.art.image_method.ImageMethod_Pie
    kSaveEverythingMethod: ghidra.file.formats.android.art.image_method.ImageMethod_Pie
    kSaveEverythingMethodForClinit: ghidra.file.formats.android.art.image_method.ImageMethod_Pie
    kSaveEverythingMethodForSuspendCheck: ghidra.file.formats.android.art.image_method.ImageMethod_Pie
    kSaveRefsAndArgsMethod: ghidra.file.formats.android.art.image_method.ImageMethod_Pie
    kSaveRefsOnlyMethod: ghidra.file.formats.android.art.image_method.ImageMethod_Pie







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

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.file.formats.android.art.image_method.ImageMethod_Pie: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.file.formats.android.art.image_method.ImageMethod_Pie]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

