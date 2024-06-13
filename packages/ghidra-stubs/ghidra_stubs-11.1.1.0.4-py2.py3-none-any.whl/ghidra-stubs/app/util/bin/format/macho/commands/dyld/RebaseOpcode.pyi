from typing import List
from typing import overload
import ghidra.app.util.bin.format.macho.commands.dyld
import ghidra.program.model.data
import java.lang
import java.util


class RebaseOpcode(java.lang.Enum):
    REBASE_OPCODE_ADD_ADDR_IMM_SCALED: ghidra.app.util.bin.format.macho.commands.dyld.RebaseOpcode
    REBASE_OPCODE_ADD_ADDR_ULEB: ghidra.app.util.bin.format.macho.commands.dyld.RebaseOpcode
    REBASE_OPCODE_DONE: ghidra.app.util.bin.format.macho.commands.dyld.RebaseOpcode
    REBASE_OPCODE_DO_REBASE_ADD_ADDR_ULEB: ghidra.app.util.bin.format.macho.commands.dyld.RebaseOpcode
    REBASE_OPCODE_DO_REBASE_IMM_TIMES: ghidra.app.util.bin.format.macho.commands.dyld.RebaseOpcode
    REBASE_OPCODE_DO_REBASE_ULEB_TIMES: ghidra.app.util.bin.format.macho.commands.dyld.RebaseOpcode
    REBASE_OPCODE_DO_REBASE_ULEB_TIMES_SKIPPING_ULEB: ghidra.app.util.bin.format.macho.commands.dyld.RebaseOpcode
    REBASE_OPCODE_SET_SEGMENT_AND_OFFSET_ULEB: ghidra.app.util.bin.format.macho.commands.dyld.RebaseOpcode
    REBASE_OPCODE_SET_TYPE_IMM: ghidra.app.util.bin.format.macho.commands.dyld.RebaseOpcode







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def forOpcode(__a0: int) -> ghidra.app.util.bin.format.macho.commands.dyld.RebaseOpcode: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def getOpcode(self) -> int: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    @staticmethod
    def toDataType() -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.macho.commands.dyld.RebaseOpcode: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.macho.commands.dyld.RebaseOpcode]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def opcode(self) -> int: ...