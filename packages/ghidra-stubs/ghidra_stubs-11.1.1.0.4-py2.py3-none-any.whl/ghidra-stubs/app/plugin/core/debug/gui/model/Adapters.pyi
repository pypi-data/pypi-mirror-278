from typing import overload
import java.awt.event
import java.lang
import javax.swing.event


class Adapters(object):





    class TreeExpansionListener(javax.swing.event.TreeExpansionListener, object):








        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def toString(self) -> unicode: ...

        def treeCollapsed(self, __a0: javax.swing.event.TreeExpansionEvent) -> None: ...

        def treeExpanded(self, __a0: javax.swing.event.TreeExpansionEvent) -> None: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class MouseListener(java.awt.event.MouseListener, object):








        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def mouseClicked(self, __a0: java.awt.event.MouseEvent) -> None: ...

        def mouseEntered(self, __a0: java.awt.event.MouseEvent) -> None: ...

        def mouseExited(self, __a0: java.awt.event.MouseEvent) -> None: ...

        def mousePressed(self, __a0: java.awt.event.MouseEvent) -> None: ...

        def mouseReleased(self, __a0: java.awt.event.MouseEvent) -> None: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class KeyListener(java.awt.event.KeyListener, object):








        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def keyPressed(self, __a0: java.awt.event.KeyEvent) -> None: ...

        def keyReleased(self, __a0: java.awt.event.KeyEvent) -> None: ...

        def keyTyped(self, __a0: java.awt.event.KeyEvent) -> None: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class FocusListener(java.awt.event.FocusListener, object):








        def equals(self, __a0: object) -> bool: ...

        def focusGained(self, __a0: java.awt.event.FocusEvent) -> None: ...

        def focusLost(self, __a0: java.awt.event.FocusEvent) -> None: ...

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

