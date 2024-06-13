from typing import overload
import ghidra.trace.util
import java.lang


class TraceEvents(object):
    BOOKMARK_ADDED: ghidra.trace.util.TraceEvent.TraceBookmarkEvent
    BOOKMARK_CHANGED: ghidra.trace.util.TraceEvent.TraceBookmarkEvent
    BOOKMARK_DELETED: ghidra.trace.util.TraceEvent.TraceBookmarkEvent
    BOOKMARK_LIFESPAN_CHANGED: ghidra.trace.util.TraceEvent.TraceBookmarkLifespanEvent
    BOOKMARK_TYPE_ADDED: ghidra.trace.util.TraceEvent.TraceBookmarkTypeEvent
    BREAKPOINT_ADDED: ghidra.trace.util.TraceEvent.TraceBreakpointEvent
    BREAKPOINT_CHANGED: ghidra.trace.util.TraceEvent.TraceBreakpointEvent
    BREAKPOINT_DELETED: ghidra.trace.util.TraceEvent.TraceBreakpointEvent
    BREAKPOINT_LIFESPAN_CHANGED: ghidra.trace.util.TraceEvent.TraceBreakpointLifespanEvent
    BYTES_CHANGED: ghidra.trace.util.TraceEvent.TraceBytesEvent
    BYTES_STATE_CHANGED: ghidra.trace.util.TraceEvent.TraceMemoryStateEvent
    CODE_ADDED: ghidra.trace.util.TraceEvent.TraceCodeEvent
    CODE_DATA_SETTINGS_CHANGED: ghidra.trace.util.TraceEvent.TraceCodeDataSettingsEvent
    CODE_DATA_TYPE_REPLACED: ghidra.trace.util.TraceEvent.TraceCodeDataTypeEvent
    CODE_FRAGMENT_CHANGED: ghidra.trace.util.TraceEvent.TraceCodeFragmentEvent
    CODE_LIFESPAN_CHANGED: ghidra.trace.util.TraceEvent.TraceCodeLifespanEvent
    CODE_REMOVED: ghidra.trace.util.TraceEvent.TraceCodeEvent
    COMPOSITE_DATA_ADDED: ghidra.trace.util.TraceEvent.TraceCompositeDataEvent
    COMPOSITE_DATA_LIFESPAN_CHANGED: ghidra.trace.util.TraceEvent.TraceCompositeDataLifespanEvent
    COMPOSITE_DATA_REMOVED: ghidra.trace.util.TraceEvent.TraceCompositeDataEvent
    DATA_TYPE_ADDED: ghidra.trace.util.TraceEvent.TraceDataTypeEvent
    DATA_TYPE_CHANGED: ghidra.trace.util.TraceEvent.TraceDataTypeEvent
    DATA_TYPE_DELETED: ghidra.trace.util.TraceEvent.TraceDataTypePathEvent
    DATA_TYPE_MOVED: ghidra.trace.util.TraceEvent.TraceDataTypePathEvent
    DATA_TYPE_RENAMED: ghidra.trace.util.TraceEvent.TraceDataTypeStringEvent
    DATA_TYPE_REPLACED: ghidra.trace.util.TraceEvent.TraceDataTypePathEvent
    EOL_COMMENT_CHANGED: ghidra.trace.util.TraceEvent.TraceCommentEvent
    INSTRUCTION_FALL_THROUGH_OVERRIDE_CHANGED: ghidra.trace.util.TraceEvent.TraceInstructionBoolEvent
    INSTRUCTION_FLOW_OVERRIDE_CHANGED: ghidra.trace.util.TraceEvent.TraceInstructionFlowEvent
    INSTRUCTION_LENGTH_OVERRIDE_CHANGED: ghidra.trace.util.TraceEvent.TraceInstructionIntEvent
    MAPPING_ADDED: ghidra.trace.util.TraceEvent.TraceMappingEvent
    MAPPING_DELETED: ghidra.trace.util.TraceEvent.TraceMappingEvent
    MODULE_ADDED: ghidra.trace.util.TraceEvent.TraceModuleEvent
    MODULE_CHANGED: ghidra.trace.util.TraceEvent.TraceModuleEvent
    MODULE_DELETED: ghidra.trace.util.TraceEvent.TraceModuleEvent
    MODULE_LIFESPAN_CHANGED: ghidra.trace.util.TraceEvent.TraceModuleLifespanEvent
    OBJECT_CREATED: ghidra.trace.util.TraceEvent.TraceObjectEvent
    OBJECT_DELETED: ghidra.trace.util.TraceEvent.TraceObjectEvent
    OBJECT_LIFE_CHANGED: ghidra.trace.util.TraceEvent.TraceObjectEvent
    OVERLAY_ADDED: ghidra.trace.util.TraceEvent.TraceOverlaySpaceEvent
    OVERLAY_DELETED: ghidra.trace.util.TraceEvent.TraceOverlaySpaceEvent
    PLATE_COMMENT_CHANGED: ghidra.trace.util.TraceEvent.TraceCommentEvent
    PLATFORM_ADDED: ghidra.trace.util.TraceEvent.TracePlatformEvent
    PLATFORM_DELETED: ghidra.trace.util.TraceEvent.TracePlatformEvent
    PLATFORM_MAPPING_ADDED: ghidra.trace.util.TraceEvent.TracePlatformMappingEvent
    PLATFORM_MAPPING_DELETED: ghidra.trace.util.TraceEvent.TracePlatformMappingEvent
    POST_COMMENT_CHANGED: ghidra.trace.util.TraceEvent.TraceCommentEvent
    PRE_COMMENT_CHANGED: ghidra.trace.util.TraceEvent.TraceCommentEvent
    REFERENCE_ADDED: ghidra.trace.util.TraceEvent.TraceReferenceEvent
    REFERENCE_DELETED: ghidra.trace.util.TraceEvent.TraceReferenceEvent
    REFERENCE_LIFESPAN_CHANGED: ghidra.trace.util.TraceEvent.TraceReferenceLifespanEvent
    REFERENCE_PRIMARY_CHANGED: ghidra.trace.util.TraceEvent.TraceReferenceBoolEvent
    REGION_ADDED: ghidra.trace.util.TraceEvent.TraceMemoryRegionEvent
    REGION_CHANGED: ghidra.trace.util.TraceEvent.TraceMemoryRegionEvent
    REGION_DELETED: ghidra.trace.util.TraceEvent.TraceMemoryRegionEvent
    REGION_LIFESPAN_CHANGED: ghidra.trace.util.TraceEvent.TraceMemoryRegionLifespanEvent
    REPEATABLE_COMMENT_CHANGED: ghidra.trace.util.TraceEvent.TraceCommentEvent
    SECTION_ADDED: ghidra.trace.util.TraceEvent.TraceSectionEvent
    SECTION_CHANGED: ghidra.trace.util.TraceEvent.TraceSectionEvent
    SECTION_DELETED: ghidra.trace.util.TraceEvent.TraceSectionEvent
    SNAPSHOT_ADDED: ghidra.trace.util.TraceEvent.TraceSnapshotEvent
    SNAPSHOT_CHANGED: ghidra.trace.util.TraceEvent.TraceSnapshotEvent
    SNAPSHOT_DELETED: ghidra.trace.util.TraceEvent.TraceSnapshotEvent
    SOURCE_TYPE_ARCHIVE_ADDED: ghidra.trace.util.TraceEvent.TraceTypeArchiveEvent
    SOURCE_TYPE_ARCHIVE_CHANGED: ghidra.trace.util.TraceEvent.TraceTypeArchiveEvent
    SOURCE_TYPE_ARCHIVE_DELETED: ghidra.trace.util.TraceEvent.TraceTypeArchiveEvent
    STACK_ADDED: ghidra.trace.util.TraceEvent.TraceStackEvent
    STACK_CHANGED: ghidra.trace.util.TraceEvent.TraceStackLongEvent
    STACK_DELETED: ghidra.trace.util.TraceEvent.TraceStackEvent
    SYMBOL_ADDED: ghidra.trace.util.TraceEvent.TraceSymbolEvent
    SYMBOL_ADDRESS_CHANGED: ghidra.trace.util.TraceEvent.TraceSymbolAddressEvent
    SYMBOL_ASSOCIATION_ADDED: ghidra.trace.util.TraceEvent.TraceSymbolRefEvent
    SYMBOL_ASSOCIATION_REMOVED: ghidra.trace.util.TraceEvent.TraceSymbolRefEvent
    SYMBOL_CHANGED: ghidra.trace.util.TraceEvent.TraceSymbolEvent
    SYMBOL_DELETED: ghidra.trace.util.TraceEvent.TraceSymbolEvent
    SYMBOL_LIFESPAN_CHANGED: ghidra.trace.util.TraceEvent.TraceSymbolLifespanEvent
    SYMBOL_PARENT_CHANGED: ghidra.trace.util.TraceEvent.TraceSymbolNamespaceEvent
    SYMBOL_PRIMARY_CHANGED: ghidra.trace.util.TraceEvent.TraceSymbolSymEvent
    SYMBOL_RENAMED: ghidra.trace.util.TraceEvent.TraceSymbolStringEvent
    SYMBOL_SOURCE_CHANGED: ghidra.trace.util.TraceEvent.TraceSymbolSourceEvent
    THREAD_ADDED: ghidra.trace.util.TraceEvent.TraceThreadEvent
    THREAD_CHANGED: ghidra.trace.util.TraceEvent.TraceThreadEvent
    THREAD_DELETED: ghidra.trace.util.TraceEvent.TraceThreadEvent
    THREAD_LIFESPAN_CHANGED: ghidra.trace.util.TraceEvent.TraceThreadLifespanEvent
    TYPE_CATEGORY_ADDED: ghidra.trace.util.TraceEvent.TraceTypeCategoryEvent
    TYPE_CATEGORY_DELETED: ghidra.trace.util.TraceEvent.TraceTypeCategoryPathEvent
    TYPE_CATEGORY_MOVED: ghidra.trace.util.TraceEvent.TraceTypeCategoryPathEvent
    TYPE_CATEGORY_RENAMED: ghidra.trace.util.TraceEvent.TraceTypeCategoryStringEvent
    VALUE_CREATED: ghidra.trace.util.TraceEvent.TraceObjectValueEvent
    VALUE_DELETED: ghidra.trace.util.TraceEvent.TraceObjectValueEvent
    VALUE_LIFESPAN_CHANGED: ghidra.trace.util.TraceEvent.TraceObjectValueLifespanEvent







    @staticmethod
    def byCommentType(__a0: int) -> ghidra.trace.util.TraceEvent.TraceCommentEvent: ...

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

