from typing import overload
import java.lang


class MarkupStatusIcons(object):
    APPLIED_ADDED_ICON: javax.swing.Icon
    APPLIED_ICON: javax.swing.Icon
    APPLIED_REPLACED_ICON: javax.swing.Icon
    APPLY_ADD_MENU_ICON: javax.swing.Icon
    APPLY_REPLACE_MENU_ICON: javax.swing.Icon
    CONFLICT_ICON: javax.swing.Icon
    DONT_CARE_ICON: javax.swing.Icon
    DONT_KNOW_ICON: javax.swing.Icon
    FAILED_ICON: javax.swing.Icon
    REJECTED_ICON: javax.swing.Icon
    SAME_ICON: javax.swing.Icon



    def __init__(self): ...



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

