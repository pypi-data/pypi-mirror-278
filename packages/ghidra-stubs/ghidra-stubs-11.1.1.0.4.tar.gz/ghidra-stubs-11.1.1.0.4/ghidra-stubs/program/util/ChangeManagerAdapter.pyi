from typing import overload
import ghidra.program.model.address
import ghidra.program.model.lang
import ghidra.program.util
import java.lang


class ChangeManagerAdapter(object, ghidra.program.util.ChangeManager):
    """
    Empty implementation for a ChangeManager.
    """

    DOCR_ADDRESS_SET_PROPERTY_MAP_ADDED: ghidra.program.util.ProgramEvent
    DOCR_ADDRESS_SET_PROPERTY_MAP_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_ADDRESS_SET_PROPERTY_MAP_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_BOOKMARK_ADDED: ghidra.program.util.ProgramEvent
    DOCR_BOOKMARK_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_BOOKMARK_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_BOOKMARK_TYPE_ADDED: ghidra.program.util.ProgramEvent
    DOCR_BOOKMARK_TYPE_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_CATEGORY_ADDED: ghidra.program.util.ProgramEvent
    DOCR_CATEGORY_MOVED: ghidra.program.util.ProgramEvent
    DOCR_CATEGORY_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_CATEGORY_RENAMED: ghidra.program.util.ProgramEvent
    DOCR_CODE_ADDED: ghidra.program.util.ProgramEvent
    DOCR_CODE_MOVED: ghidra.program.util.ProgramEvent
    DOCR_CODE_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_CODE_REPLACED: ghidra.program.util.ProgramEvent
    DOCR_CODE_UNIT_PROPERTY_ALL_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_CODE_UNIT_PROPERTY_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_CODE_UNIT_PROPERTY_RANGE_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_CODE_UNIT_USER_DATA_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_COMPOSITE_ADDED: ghidra.program.util.ProgramEvent
    DOCR_COMPOSITE_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_DATA_TYPE_ADDED: ghidra.program.util.ProgramEvent
    DOCR_DATA_TYPE_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_DATA_TYPE_MOVED: ghidra.program.util.ProgramEvent
    DOCR_DATA_TYPE_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_DATA_TYPE_RENAMED: ghidra.program.util.ProgramEvent
    DOCR_DATA_TYPE_REPLACED: ghidra.program.util.ProgramEvent
    DOCR_DATA_TYPE_SETTING_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_EOL_COMMENT_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_EQUATE_ADDED: ghidra.program.util.ProgramEvent
    DOCR_EQUATE_REFERENCE_ADDED: ghidra.program.util.ProgramEvent
    DOCR_EQUATE_REFERENCE_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_EQUATE_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_EQUATE_RENAMED: ghidra.program.util.ProgramEvent
    DOCR_EXTERNAL_ENTRY_POINT_ADDED: ghidra.program.util.ProgramEvent
    DOCR_EXTERNAL_ENTRY_POINT_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_EXTERNAL_NAME_ADDED: ghidra.program.util.ProgramEvent
    DOCR_EXTERNAL_NAME_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_EXTERNAL_NAME_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_EXTERNAL_PATH_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_EXTERNAL_REFERENCE_ADDED: ghidra.program.util.ProgramEvent
    DOCR_EXTERNAL_REFERENCE_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_FALLTHROUGH_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_FLOWOVERRIDE_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_FRAGMENT_MOVED: ghidra.program.util.ProgramEvent
    DOCR_FUNCTION_ADDED: ghidra.program.util.ProgramEvent
    DOCR_FUNCTION_BODY_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_FUNCTION_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_FUNCTION_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_FUNCTION_TAG_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_FUNCTION_TAG_CREATED: ghidra.program.util.ProgramEvent
    DOCR_FUNCTION_TAG_DELETED: ghidra.program.util.ProgramEvent
    DOCR_GROUP_ADDED: ghidra.program.util.ProgramEvent
    DOCR_GROUP_ALIAS_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_GROUP_COMMENT_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_GROUP_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_GROUP_RENAMED: ghidra.program.util.ProgramEvent
    DOCR_GROUP_REPARENTED: ghidra.program.util.ProgramEvent
    DOCR_IMAGE_BASE_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_INT_ADDRESS_SET_PROPERTY_MAP_ADDED: ghidra.program.util.ProgramEvent
    DOCR_INT_ADDRESS_SET_PROPERTY_MAP_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_INT_ADDRESS_SET_PROPERTY_MAP_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_LANGUAGE_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_LENGTH_OVERRIDE_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_MEMORY_BLOCKS_JOINED: ghidra.program.util.ProgramEvent
    DOCR_MEMORY_BLOCK_ADDED: ghidra.program.util.ProgramEvent
    DOCR_MEMORY_BLOCK_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_MEMORY_BLOCK_MOVED: ghidra.program.util.ProgramEvent
    DOCR_MEMORY_BLOCK_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_MEMORY_BLOCK_SPLIT: ghidra.program.util.ProgramEvent
    DOCR_MEMORY_BYTES_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_MEM_REFERENCE_ADDED: ghidra.program.util.ProgramEvent
    DOCR_MEM_REFERENCE_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_MEM_REF_PRIMARY_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_MEM_REF_PRIMARY_SET: ghidra.program.util.ProgramEvent
    DOCR_MEM_REF_TYPE_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_MODULE_REORDERED: ghidra.program.util.ProgramEvent
    DOCR_OVERLAY_SPACE_ADDED: ghidra.program.util.ProgramEvent
    DOCR_OVERLAY_SPACE_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_OVERLAY_SPACE_RENAMED: ghidra.program.util.ProgramEvent
    DOCR_PLATE_COMMENT_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_POST_COMMENT_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_PRE_COMMENT_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_REGISTER_VALUES_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_REPEATABLE_COMMENT_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_SOURCE_ARCHIVE_ADDED: ghidra.program.util.ProgramEvent
    DOCR_SOURCE_ARCHIVE_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_SYMBOL_ADDED: ghidra.program.util.ProgramEvent
    DOCR_SYMBOL_ADDRESS_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_SYMBOL_ANCHORED_FLAG_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_SYMBOL_ASSOCIATION_ADDED: ghidra.program.util.ProgramEvent
    DOCR_SYMBOL_ASSOCIATION_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_SYMBOL_DATA_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_SYMBOL_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_SYMBOL_RENAMED: ghidra.program.util.ProgramEvent
    DOCR_SYMBOL_SCOPE_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_SYMBOL_SET_AS_PRIMARY: ghidra.program.util.ProgramEvent
    DOCR_SYMBOL_SOURCE_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_TREE_CREATED: ghidra.program.util.ProgramEvent
    DOCR_TREE_REMOVED: ghidra.program.util.ProgramEvent
    DOCR_TREE_RENAMED: ghidra.program.util.ProgramEvent
    DOCR_USER_DATA_CHANGED: ghidra.program.util.ProgramEvent
    DOCR_VARIABLE_REFERENCE_ADDED: ghidra.program.util.ProgramEvent
    DOCR_VARIABLE_REFERENCE_REMOVED: ghidra.program.util.ProgramEvent
    FUNCTION_CHANGED_CALL_FIXUP: ghidra.program.util.FunctionChangeRecord.FunctionChangeType
    FUNCTION_CHANGED_INLINE: ghidra.program.util.FunctionChangeRecord.FunctionChangeType
    FUNCTION_CHANGED_NORETURN: ghidra.program.util.FunctionChangeRecord.FunctionChangeType
    FUNCTION_CHANGED_PARAMETERS: ghidra.program.util.FunctionChangeRecord.FunctionChangeType
    FUNCTION_CHANGED_PURGE: ghidra.program.util.FunctionChangeRecord.FunctionChangeType
    FUNCTION_CHANGED_RETURN: ghidra.program.util.FunctionChangeRecord.FunctionChangeType
    FUNCTION_CHANGED_THUNK: ghidra.program.util.FunctionChangeRecord.FunctionChangeType



    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    def setChanged(self, event: ghidra.program.util.ProgramEvent, oldValue: object, newValue: object) -> None: ...

    @overload
    def setChanged(self, event: ghidra.program.util.ProgramEvent, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address, oldValue: object, newValue: object) -> None: ...

    @overload
    def setObjChanged(self, event: ghidra.program.util.ProgramEvent, affected: object, oldValue: object, newValue: object) -> None: ...

    @overload
    def setObjChanged(self, eventType: ghidra.program.util.ProgramEvent, addr: ghidra.program.model.address.Address, affected: object, oldValue: object, newValue: object) -> None: ...

    def setPropertyChanged(self, propertyName: unicode, codeUnitAddr: ghidra.program.model.address.Address, oldValue: object, newValue: object) -> None: ...

    def setPropertyRangeRemoved(self, propertyName: unicode, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address) -> None: ...

    def setRegisterValuesChanged(self, register: ghidra.program.model.lang.Register, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

