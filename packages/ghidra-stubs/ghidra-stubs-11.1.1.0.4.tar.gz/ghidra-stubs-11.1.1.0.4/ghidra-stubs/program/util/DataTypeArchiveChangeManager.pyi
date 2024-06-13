from typing import overload
import java.lang


class DataTypeArchiveChangeManager(object):
    """
    Interface to define event types and the method to generate an
     event within Program.
    """

    DOCR_CATEGORY_ADDED: ghidra.program.util.ProgramEvent
    DOCR_CATEGORY_MOVED: ghidra.program.util.ProgramEvent
    DOCR_CATEGORY_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_CATEGORY_RENAMED: ghidra.program.util.ProgramEvent
    DOCR_DATA_TYPE_ADDED: ghidra.program.util.ProgramEvent
    DOCR_DATA_TYPE_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_DATA_TYPE_MOVED: ghidra.program.util.ProgramEvent
    DOCR_DATA_TYPE_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_DATA_TYPE_RENAMED: ghidra.program.util.ProgramEvent
    DOCR_DATA_TYPE_REPLACED: ghidra.program.util.ProgramEvent
    DOCR_DATA_TYPE_SETTING_CHANGED: ghidra.program.util.ProgramEvent







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

