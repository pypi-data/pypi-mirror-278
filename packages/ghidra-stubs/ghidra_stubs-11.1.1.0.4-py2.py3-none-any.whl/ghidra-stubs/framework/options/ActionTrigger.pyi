from typing import overload
import ghidra.framework.options
import gui.event
import java.lang
import javax.swing


class ActionTrigger(object):
    """
    Represents a way to trigger an action in the system.  A trigger is based on a key stroke, a mouse 
     binding or both.
    """





    @overload
    def __init__(self, mouseBinding: gui.event.MouseBinding):
        """
        Creates an action trigger with the given mouse binding.
        @param mouseBinding the mouse binding
        """
        ...

    @overload
    def __init__(self, keyStroke: javax.swing.KeyStroke):
        """
        Creates an action trigger with the given key stroke.
        @param keyStroke the key stroke
        """
        ...

    @overload
    def __init__(self, keyStroke: javax.swing.KeyStroke, mouseBinding: gui.event.MouseBinding):
        """
        A convenience constructor for creating an action trigger with either or both values set.  At
         least one of the values must be non-null.
        @param keyStroke the key stroke; may be null
        @param mouseBinding the mouse binding; may be null
        """
        ...



    @staticmethod
    def create(saveState: ghidra.framework.options.SaveState) -> ghidra.framework.options.ActionTrigger:
        """
        Creates a new action trigger by reading data from the given save state.
        @param saveState the save state
        @return the new action trigger
        """
        ...

    def equals(self, obj: object) -> bool: ...

    @staticmethod
    def getActionTrigger(string: unicode) -> ghidra.framework.options.ActionTrigger:
        """
        Creates a new action trigger from the given string.  The string is expected to be the result
         of calling {@link #toString()} on an instance of this class.
        @param string the string to parse.
        @return the new instance or null of the string is invalid.
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getKeyStroke(self) -> javax.swing.KeyStroke: ...

    def getMouseBinding(self) -> gui.event.MouseBinding: ...

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

    def writeState(self, saveState: ghidra.framework.options.SaveState) -> None:
        """
        Writes this action trigger's data into the given save state.
        @param saveState the save state
        """
        ...

    @property
    def keyStroke(self) -> javax.swing.KeyStroke: ...

    @property
    def mouseBinding(self) -> gui.event.MouseBinding: ...