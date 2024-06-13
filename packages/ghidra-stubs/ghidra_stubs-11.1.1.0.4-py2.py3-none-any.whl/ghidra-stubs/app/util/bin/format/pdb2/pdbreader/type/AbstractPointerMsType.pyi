from typing import List
from typing import overload
import ghidra.app.util.bin.format.pdb2.pdbreader
import ghidra.app.util.bin.format.pdb2.pdbreader.type
import java.lang
import java.util


class AbstractPointerMsType(ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractMsType):





    class MsPointerMode(java.lang.Enum):
        INVALID: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MsPointerMode
        LVALUE_REFERENCE: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MsPointerMode
        MEMBER_DATA_POINTER: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MsPointerMode
        MEMBER_FUNCTION_POINTER: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MsPointerMode
        POINTER: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MsPointerMode
        RESERVED: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MsPointerMode
        RVALUE_REFERENCE: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MsPointerMode
        label: unicode
        value: int







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def emit(self, __a0: java.lang.StringBuilder) -> None: ...

        def equals(self, __a0: object) -> bool: ...

        @staticmethod
        def fromValue(__a0: int) -> ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MsPointerMode: ...

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
        def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MsPointerMode: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MsPointerMode]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class PointerType(java.lang.Enum):
        ADDRESS_BASED: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType
        FAR: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType
        FAR32: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType
        HUGE: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType
        INVALID: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType
        NEAR: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType
        NEAR32: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType
        PTR64: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType
        SEGMENT_ADDRESS_BASED: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType
        SEGMENT_BASED: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType
        SEGMENT_VALUE_BASED: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType
        SELF_BASED: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType
        TYPE_BASED: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType
        UNSPECIFIED: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType
        VALUE_BASED: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType
        label: unicode
        value: int







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        @staticmethod
        def fromValue(__a0: int) -> ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType: ...

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
        def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class MemberPointerType(java.lang.Enum):
        DATA_GENERAL: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType
        DATA_MULTIPLE_INHERITANCE: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType
        DATA_SINGLE_INHERITANCE: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType
        DATA_VIRTUAL_INHERITANCE: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType
        FUNCTION_MULTIPLE_INHERITANCE: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType
        FUNCTION_MULTIPLE_INHERITANCE_1632: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType
        FUNCTION_MULTIPLE_INHERITANCE_32: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType
        FUNCTION_SINGLE_INHERITANCE: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType
        FUNCTION_SINGLE_INHERITANCE_1632: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType
        FUNCTION_SINGLE_INHERITANCE_32: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType
        FUNCTION_VIRTUAL_INHERITANCE: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType
        FUNCTION_VIRTUAL_INHERITANCE_1632: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType
        FUNCTION_VIRTUAL_INHERITANCE_32: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType
        INVALID: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType
        UNSPECIFIED: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType
        label: unicode
        value: int







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        @staticmethod
        def fromValue(__a0: int) -> ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType: ...

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
        def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...



    def __init__(self, __a0: ghidra.app.util.bin.format.pdb2.pdbreader.AbstractPdb, __a1: ghidra.app.util.bin.format.pdb2.pdbreader.PdbByteReader): ...



    @overload
    def emit(self, __a0: java.lang.StringBuilder) -> None: ...

    @overload
    def emit(self, __a0: java.lang.StringBuilder, __a1: ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractMsType.Bind) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getLength(self) -> long: ...

    def getMemberPointerContainingClassRecordNumber(self) -> ghidra.app.util.bin.format.pdb2.pdbreader.RecordNumber: ...

    def getMemberPointerType(self) -> ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType: ...

    def getName(self) -> unicode: ...

    def getPdbId(self) -> int: ...

    def getPointerMode(self) -> ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MsPointerMode: ...

    def getPointerType(self) -> ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType: ...

    def getRecordNumber(self) -> ghidra.app.util.bin.format.pdb2.pdbreader.RecordNumber: ...

    def getSize(self) -> long: ...

    def getUnderlyingRecordNumber(self) -> ghidra.app.util.bin.format.pdb2.pdbreader.RecordNumber: ...

    def getUnderlyingType(self) -> ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractMsType: ...

    def hashCode(self) -> int: ...

    def isConst(self) -> bool: ...

    def isFlat(self) -> bool: ...

    def isUnaligned(self) -> bool: ...

    def isVolatile(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parseExtendedPointerInfo(self, __a0: ghidra.app.util.bin.format.pdb2.pdbreader.PdbByteReader, __a1: int, __a2: ghidra.app.util.bin.format.pdb2.pdbreader.StringParseType) -> None: ...

    def setRecordNumber(self, __a0: ghidra.app.util.bin.format.pdb2.pdbreader.RecordNumber) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def const(self) -> bool: ...

    @property
    def flat(self) -> bool: ...

    @property
    def memberPointerContainingClassRecordNumber(self) -> ghidra.app.util.bin.format.pdb2.pdbreader.RecordNumber: ...

    @property
    def memberPointerType(self) -> ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MemberPointerType: ...

    @property
    def pointerMode(self) -> ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.MsPointerMode: ...

    @property
    def pointerType(self) -> ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractPointerMsType.PointerType: ...

    @property
    def size(self) -> long: ...

    @property
    def unaligned(self) -> bool: ...

    @property
    def underlyingRecordNumber(self) -> ghidra.app.util.bin.format.pdb2.pdbreader.RecordNumber: ...

    @property
    def underlyingType(self) -> ghidra.app.util.bin.format.pdb2.pdbreader.type.AbstractMsType: ...

    @property
    def volatile(self) -> bool: ...