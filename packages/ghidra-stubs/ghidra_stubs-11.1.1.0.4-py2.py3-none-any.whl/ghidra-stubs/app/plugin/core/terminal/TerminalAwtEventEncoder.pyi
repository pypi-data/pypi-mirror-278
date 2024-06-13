from typing import List
from typing import overload
import ghidra.app.plugin.core.terminal.vt
import java.awt.event
import java.lang


class TerminalAwtEventEncoder(object):
    CODE_DELETE: List[int]
    CODE_DOWN_APPLICATION: List[int]
    CODE_DOWN_NORMAL: List[int]
    CODE_END_APPLICATION: List[int]
    CODE_END_NORMAL: List[int]
    CODE_ENTER: List[int]
    CODE_F1: List[int]
    CODE_F10: List[int]
    CODE_F11: List[int]
    CODE_F12: List[int]
    CODE_F13: List[int]
    CODE_F14: List[int]
    CODE_F15: List[int]
    CODE_F16: List[int]
    CODE_F17: List[int]
    CODE_F18: List[int]
    CODE_F19: List[int]
    CODE_F2: List[int]
    CODE_F20: List[int]
    CODE_F3: List[int]
    CODE_F4: List[int]
    CODE_F5: List[int]
    CODE_F6: List[int]
    CODE_F7: List[int]
    CODE_F8: List[int]
    CODE_F9: List[int]
    CODE_FOCUS_GAINED: List[int]
    CODE_FOCUS_LOST: List[int]
    CODE_HOME_APPLICATION: List[int]
    CODE_HOME_NORMAL: List[int]
    CODE_INSERT: List[int]
    CODE_LEFT_APPLICATION: List[int]
    CODE_LEFT_NORMAL: List[int]
    CODE_NONE: List[int]
    CODE_NUMPAD5: List[int]
    CODE_PAGE_DOWN: List[int]
    CODE_PAGE_UP: List[int]
    CODE_RIGHT_APPLICATION: List[int]
    CODE_RIGHT_NORMAL: List[int]
    CODE_UP_APPLICATION: List[int]
    CODE_UP_NORMAL: List[int]
    ESC: int = 27



    @overload
    def __init__(self, __a0: unicode): ...

    @overload
    def __init__(self, __a0: java.nio.charset.Charset): ...



    def equals(self, __a0: object) -> bool: ...

    def focusGained(self) -> None: ...

    def focusLost(self) -> None: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def keyPressed(self, __a0: java.awt.event.KeyEvent, __a1: ghidra.app.plugin.core.terminal.vt.VtHandler.KeyMode, __a2: ghidra.app.plugin.core.terminal.vt.VtHandler.KeyMode) -> None: ...

    def keyTyped(self, __a0: java.awt.event.KeyEvent) -> None: ...

    def mousePressed(self, __a0: java.awt.event.MouseEvent, __a1: int, __a2: int) -> None: ...

    def mouseReleased(self, __a0: java.awt.event.MouseEvent, __a1: int, __a2: int) -> None: ...

    def mouseWheelMoved(self, __a0: java.awt.event.MouseWheelEvent, __a1: int, __a2: int) -> None: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def sendChar(self, __a0: int) -> None: ...

    def sendText(self, __a0: java.lang.CharSequence) -> None: ...

    def toString(self) -> unicode: ...

    @staticmethod
    def vtseq(__a0: int) -> List[int]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

