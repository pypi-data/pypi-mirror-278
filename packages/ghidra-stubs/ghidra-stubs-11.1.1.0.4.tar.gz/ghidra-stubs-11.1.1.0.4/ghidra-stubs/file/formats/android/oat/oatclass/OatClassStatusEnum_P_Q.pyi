from typing import List
from typing import overload
import ghidra.file.formats.android.oat.oatclass
import ghidra.program.model.data
import java.lang
import java.util


class OatClassStatusEnum_P_Q(java.lang.Enum, ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum):
    kErrorResolved: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q
    kErrorUnresolved: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q
    kIdx: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q
    kInitialized: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q
    kInitializing: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q
    kLast: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q
    kLoaded: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q
    kNotReady: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q
    kResolved: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q
    kResolving: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q
    kRetired: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q
    kRetryVerificationAtRuntime: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q
    kSuperclassValidated: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q
    kVerified: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q
    kVerifying: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q
    kVerifyingAtRuntime: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def get(self, __a0: int) -> ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def getValue(self) -> int: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_P_Q]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def value(self) -> int: ...