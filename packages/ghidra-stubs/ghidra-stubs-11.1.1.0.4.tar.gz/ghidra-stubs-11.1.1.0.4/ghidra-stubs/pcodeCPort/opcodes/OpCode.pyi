from typing import List
from typing import overload
import ghidra.pcodeCPort.opcodes
import java.lang
import java.util


class OpCode(java.lang.Enum):
    CPUI_BOOL_AND: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_BOOL_NEGATE: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_BOOL_OR: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_BOOL_XOR: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_BRANCH: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_BRANCHIND: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_CALL: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_CALLIND: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_CALLOTHER: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_CAST: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_CBRANCH: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_COPY: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_CPOOLREF: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_EXTRACT: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_ABS: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_ADD: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_CEIL: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_DIV: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_EQUAL: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_FLOAT2FLOAT: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_FLOOR: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_INT2FLOAT: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_LESS: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_LESSEQUAL: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_MULT: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_NAN: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_NEG: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_NOTEQUAL: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_ROUND: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_SQRT: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_SUB: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_FLOAT_TRUNC: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INDIRECT: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INSERT: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_2COMP: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_ADD: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_AND: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_CARRY: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_DIV: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_EQUAL: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_LEFT: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_LESS: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_LESSEQUAL: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_MULT: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_NEGATE: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_NOTEQUAL: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_OR: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_REM: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_RIGHT: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_SBORROW: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_SCARRY: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_SDIV: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_SEXT: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_SLESS: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_SLESSEQUAL: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_SREM: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_SRIGHT: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_SUB: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_XOR: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_INT_ZEXT: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_LOAD: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_LZCOUNT: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_MAX: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_MULTIEQUAL: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_NEW: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_PIECE: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_POPCOUNT: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_PTRADD: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_PTRSUB: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_RETURN: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_SEGMENTOP: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_STORE: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_SUBPIECE: ghidra.pcodeCPort.opcodes.OpCode
    CPUI_UNUSED1: ghidra.pcodeCPort.opcodes.OpCode
    DO_NOT_USE_ME_I_AM_ENUM_ELEMENT_ZERO: ghidra.pcodeCPort.opcodes.OpCode







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getBooleanFlip(self) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def getName(self) -> unicode: ...

    def getOpCodeFlip(self) -> ghidra.pcodeCPort.opcodes.OpCode: ...

    @staticmethod
    def get_opcode(__a0: unicode) -> ghidra.pcodeCPort.opcodes.OpCode: ...

    @staticmethod
    def get_opname(__a0: ghidra.pcodeCPort.opcodes.OpCode) -> unicode: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.pcodeCPort.opcodes.OpCode: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.pcodeCPort.opcodes.OpCode]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def booleanFlip(self) -> bool: ...

    @property
    def opCodeFlip(self) -> ghidra.pcodeCPort.opcodes.OpCode: ...