from typing import List
from typing import overload
import ghidra.file.formats.android.oat.oatclass
import ghidra.program.model.data
import java.lang
import java.util


class OatClassStatusEnum_L_M_N(java.lang.Enum, ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum):
    kStatusError: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_L_M_N
    kStatusIdx: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_L_M_N
    kStatusInitialized: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_L_M_N
    kStatusInitializing: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_L_M_N
    kStatusLoaded: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_L_M_N
    kStatusMax: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_L_M_N
    kStatusNotReady: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_L_M_N
    kStatusResolved: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_L_M_N
    kStatusResolving: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_L_M_N
    kStatusRetired: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_L_M_N
    kStatusRetryVerificationAtRuntime: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_L_M_N
    kStatusVerified: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_L_M_N
    kStatusVerifying: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_L_M_N
    kStatusVerifyingAtRuntime: ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_L_M_N







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
    def valueOf(__a0: unicode) -> ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_L_M_N: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.file.formats.android.oat.oatclass.OatClassStatusEnum_L_M_N]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def value(self) -> int: ...