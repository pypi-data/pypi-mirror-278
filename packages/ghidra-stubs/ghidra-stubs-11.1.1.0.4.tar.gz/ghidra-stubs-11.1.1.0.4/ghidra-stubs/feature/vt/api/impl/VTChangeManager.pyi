from typing import overload
import java.lang


class VTChangeManager(object):
    DOCR_VT_ASSOCIATION_ADDED: ghidra.feature.vt.api.impl.VTEvent
    DOCR_VT_ASSOCIATION_MARKUP_STATUS_CHANGED: ghidra.feature.vt.api.impl.VTEvent
    DOCR_VT_ASSOCIATION_REMOVED: ghidra.feature.vt.api.impl.VTEvent
    DOCR_VT_ASSOCIATION_STATUS_CHANGED: ghidra.feature.vt.api.impl.VTEvent
    DOCR_VT_MARKUP_ITEM_DESTINATION_CHANGED: ghidra.feature.vt.api.impl.VTEvent
    DOCR_VT_MARKUP_ITEM_STATUS_CHANGED: ghidra.feature.vt.api.impl.VTEvent
    DOCR_VT_MATCH_ADDED: ghidra.feature.vt.api.impl.VTEvent
    DOCR_VT_MATCH_DELETED: ghidra.feature.vt.api.impl.VTEvent
    DOCR_VT_MATCH_SET_ADDED: ghidra.feature.vt.api.impl.VTEvent
    DOCR_VT_MATCH_TAG_CHANGED: ghidra.feature.vt.api.impl.VTEvent
    DOCR_VT_TAG_ADDED: ghidra.feature.vt.api.impl.VTEvent
    DOCR_VT_TAG_REMOVED: ghidra.feature.vt.api.impl.VTEvent
    DOCR_VT_VOTE_COUNT_CHANGED: ghidra.feature.vt.api.impl.VTEvent







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

