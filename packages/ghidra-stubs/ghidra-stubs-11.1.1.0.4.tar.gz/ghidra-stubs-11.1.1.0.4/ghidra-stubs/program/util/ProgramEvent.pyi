from typing import List
from typing import overload
import ghidra.framework.model
import ghidra.program.util
import java.lang
import java.util


class ProgramEvent(java.lang.Enum, ghidra.framework.model.EventType):
    ADDRESS_PROPERTY_MAP_ADDED: ghidra.program.util.ProgramEvent
    ADDRESS_PROPERTY_MAP_CHANGED: ghidra.program.util.ProgramEvent
    ADDRESS_PROPERTY_MAP_REMOVED: ghidra.program.util.ProgramEvent
    BOOKMARK_ADDED: ghidra.program.util.ProgramEvent
    BOOKMARK_CHANGED: ghidra.program.util.ProgramEvent
    BOOKMARK_REMOVED: ghidra.program.util.ProgramEvent
    BOOKMARK_TYPE_ADDED: ghidra.program.util.ProgramEvent
    BOOKMARK_TYPE_REMOVED: ghidra.program.util.ProgramEvent
    CODE_ADDED: ghidra.program.util.ProgramEvent
    CODE_REMOVED: ghidra.program.util.ProgramEvent
    CODE_REPLACED: ghidra.program.util.ProgramEvent
    CODE_UNIT_PROPERTY_ALL_REMOVED: ghidra.program.util.ProgramEvent
    CODE_UNIT_PROPERTY_CHANGED: ghidra.program.util.ProgramEvent
    CODE_UNIT_PROPERTY_RANGE_REMOVED: ghidra.program.util.ProgramEvent
    CODE_UNIT_USER_DATA_CHANGED: ghidra.program.util.ProgramEvent
    COMMENT_CHANGED: ghidra.program.util.ProgramEvent
    COMPOSITE_ADDED: ghidra.program.util.ProgramEvent
    COMPOSITE_REMOVED: ghidra.program.util.ProgramEvent
    DATA_TYPE_ADDED: ghidra.program.util.ProgramEvent
    DATA_TYPE_CATEGORY_ADDED: ghidra.program.util.ProgramEvent
    DATA_TYPE_CATEGORY_MOVED: ghidra.program.util.ProgramEvent
    DATA_TYPE_CATEGORY_REMOVED: ghidra.program.util.ProgramEvent
    DATA_TYPE_CATEGORY_RENAMED: ghidra.program.util.ProgramEvent
    DATA_TYPE_CHANGED: ghidra.program.util.ProgramEvent
    DATA_TYPE_MOVED: ghidra.program.util.ProgramEvent
    DATA_TYPE_REMOVED: ghidra.program.util.ProgramEvent
    DATA_TYPE_RENAMED: ghidra.program.util.ProgramEvent
    DATA_TYPE_REPLACED: ghidra.program.util.ProgramEvent
    DATA_TYPE_SETTING_CHANGED: ghidra.program.util.ProgramEvent
    EQUATE_ADDED: ghidra.program.util.ProgramEvent
    EQUATE_REFERENCE_ADDED: ghidra.program.util.ProgramEvent
    EQUATE_REFERENCE_REMOVED: ghidra.program.util.ProgramEvent
    EQUATE_REMOVED: ghidra.program.util.ProgramEvent
    EQUATE_RENAMED: ghidra.program.util.ProgramEvent
    EXTERNAL_ENTRY_ADDED: ghidra.program.util.ProgramEvent
    EXTERNAL_ENTRY_REMOVED: ghidra.program.util.ProgramEvent
    EXTERNAL_NAME_ADDED: ghidra.program.util.ProgramEvent
    EXTERNAL_NAME_CHANGED: ghidra.program.util.ProgramEvent
    EXTERNAL_NAME_REMOVED: ghidra.program.util.ProgramEvent
    EXTERNAL_PATH_CHANGED: ghidra.program.util.ProgramEvent
    EXTERNAL_REFERENCE_ADDED: ghidra.program.util.ProgramEvent
    EXTERNAL_REFERENCE_REMOVED: ghidra.program.util.ProgramEvent
    FALLTHROUGH_CHANGED: ghidra.program.util.ProgramEvent
    FLOW_OVERRIDE_CHANGED: ghidra.program.util.ProgramEvent
    FRAGMENT_CHANGED: ghidra.program.util.ProgramEvent
    FRAGMENT_MOVED: ghidra.program.util.ProgramEvent
    FUNCTION_ADDED: ghidra.program.util.ProgramEvent
    FUNCTION_BODY_CHANGED: ghidra.program.util.ProgramEvent
    FUNCTION_CHANGED: ghidra.program.util.ProgramEvent
    FUNCTION_REMOVED: ghidra.program.util.ProgramEvent
    FUNCTION_TAG_APPLIED: ghidra.program.util.ProgramEvent
    FUNCTION_TAG_CHANGED: ghidra.program.util.ProgramEvent
    FUNCTION_TAG_CREATED: ghidra.program.util.ProgramEvent
    FUNCTION_TAG_DELETED: ghidra.program.util.ProgramEvent
    FUNCTION_TAG_UNAPPLIED: ghidra.program.util.ProgramEvent
    GROUP_ADDED: ghidra.program.util.ProgramEvent
    GROUP_ALIAS_CHANGED: ghidra.program.util.ProgramEvent
    GROUP_COMMENT_CHANGED: ghidra.program.util.ProgramEvent
    GROUP_REMOVED: ghidra.program.util.ProgramEvent
    GROUP_RENAMED: ghidra.program.util.ProgramEvent
    GROUP_REPARENTED: ghidra.program.util.ProgramEvent
    IMAGE_BASE_CHANGED: ghidra.program.util.ProgramEvent
    INT_PROPERTY_MAP_ADDED: ghidra.program.util.ProgramEvent
    INT_PROPERTY_MAP_CHANGED: ghidra.program.util.ProgramEvent
    INT_PROPERTY_MAP_REMOVED: ghidra.program.util.ProgramEvent
    LANGUAGE_CHANGED: ghidra.program.util.ProgramEvent
    LENGTH_OVERRIDE_CHANGED: ghidra.program.util.ProgramEvent
    MEMORY_BLOCKS_JOINED: ghidra.program.util.ProgramEvent
    MEMORY_BLOCK_ADDED: ghidra.program.util.ProgramEvent
    MEMORY_BLOCK_CHANGED: ghidra.program.util.ProgramEvent
    MEMORY_BLOCK_MOVED: ghidra.program.util.ProgramEvent
    MEMORY_BLOCK_REMOVED: ghidra.program.util.ProgramEvent
    MEMORY_BLOCK_SPLIT: ghidra.program.util.ProgramEvent
    MEMORY_BYTES_CHANGED: ghidra.program.util.ProgramEvent
    MODULE_REORDERED: ghidra.program.util.ProgramEvent
    OVERLAY_SPACE_ADDED: ghidra.program.util.ProgramEvent
    OVERLAY_SPACE_REMOVED: ghidra.program.util.ProgramEvent
    OVERLAY_SPACE_RENAMED: ghidra.program.util.ProgramEvent
    PROGRAM_TREE_CREATED: ghidra.program.util.ProgramEvent
    PROGRAM_TREE_REMOVED: ghidra.program.util.ProgramEvent
    PROGRAM_TREE_RENAMED: ghidra.program.util.ProgramEvent
    REFERENCE_ADDED: ghidra.program.util.ProgramEvent
    REFERENCE_PRIMARY_REMOVED: ghidra.program.util.ProgramEvent
    REFERENCE_REMOVED: ghidra.program.util.ProgramEvent
    REFERENCE_TYPE_CHANGED: ghidra.program.util.ProgramEvent
    REFERNCE_PRIMARY_SET: ghidra.program.util.ProgramEvent
    REGISTER_VALUES_CHANGED: ghidra.program.util.ProgramEvent
    RELOCATION_ADDED: ghidra.program.util.ProgramEvent
    SOURCE_ARCHIVE_ADDED: ghidra.program.util.ProgramEvent
    SOURCE_ARCHIVE_CHANGED: ghidra.program.util.ProgramEvent
    SYMBOL_ADDED: ghidra.program.util.ProgramEvent
    SYMBOL_ADDRESS_CHANGED: ghidra.program.util.ProgramEvent
    SYMBOL_ANCHOR_FLAG_CHANGED: ghidra.program.util.ProgramEvent
    SYMBOL_ASSOCIATION_ADDED: ghidra.program.util.ProgramEvent
    SYMBOL_ASSOCIATION_REMOVED: ghidra.program.util.ProgramEvent
    SYMBOL_DATA_CHANGED: ghidra.program.util.ProgramEvent
    SYMBOL_PRIMARY_STATE_CHANGED: ghidra.program.util.ProgramEvent
    SYMBOL_REMOVED: ghidra.program.util.ProgramEvent
    SYMBOL_RENAMED: ghidra.program.util.ProgramEvent
    SYMBOL_SCOPE_CHANGED: ghidra.program.util.ProgramEvent
    SYMBOL_SOURCE_CHANGED: ghidra.program.util.ProgramEvent
    USER_DATA_CHANGED: ghidra.program.util.ProgramEvent
    VARIABLE_REFERENCE_ADDED: ghidra.program.util.ProgramEvent
    VARIABLE_REFERENCE_REMOVED: ghidra.program.util.ProgramEvent







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def getId(self) -> int: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.program.util.ProgramEvent: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.program.util.ProgramEvent]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def id(self) -> int: ...