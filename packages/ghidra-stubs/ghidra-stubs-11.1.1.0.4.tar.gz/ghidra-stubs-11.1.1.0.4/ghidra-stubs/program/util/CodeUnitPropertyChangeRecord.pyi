from typing import overload
import ghidra.framework.model
import ghidra.program.model.address
import ghidra.program.util
import java.lang


class CodeUnitPropertyChangeRecord(ghidra.program.util.ProgramChangeRecord):
    """
    Change record generated when a property on a code unit changes.
    """





    @overload
    def __init__(self, type: ghidra.program.util.ProgramEvent, propertyName: unicode, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address):
        """
        Constructor for events that affect a range of values
        @param type the program event type
        @param propertyName the name of the code unit property
        @param start the start address of the range affected
        @param end the end address of the range affected
        """
        ...

    @overload
    def __init__(self, type: ghidra.program.util.ProgramEvent, propertyName: unicode, address: ghidra.program.model.address.Address, oldValue: object, newValue: object):
        """
        Constructor for a property change at an address
        @param type the program event type
        @param propertyName the name of the code unit property
        @param address the address of the of the property that was changed.
        @param oldValue the old property value
        @param newValue the new property value
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getEnd(self) -> ghidra.program.model.address.Address:
        """
        Get the end address of the affected addresses of this change or null if not applicable.
        @return the end address of the effected address of this change
        """
        ...

    def getEventType(self) -> ghidra.framework.model.EventType:
        """
        Returns the event type for this change.
        @return the event type for this change
        """
        ...

    def getNewValue(self) -> object:
        """
        Return the new value for this event or null if not applicable.
        @return the old value or null if not applicable for this event.
        """
        ...

    def getObject(self) -> object:
        """
        Return the object that is the subject of this change record.
        @return the object affected or null if not applicable
        """
        ...

    def getOldValue(self) -> object:
        """
        Return the old value for this event or null if not applicable.
        @return the old value or null if not applicable
        """
        ...

    def getPropertyName(self) -> unicode:
        """
        Get the name of the property being changed.
        @return the name of the property being changed
        """
        ...

    def getStart(self) -> ghidra.program.model.address.Address:
        """
        Get the start address of the affected addresses of this change or null if not applicable.
        @return the start address of the effected address of this change
        """
        ...

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

    @property
    def propertyName(self) -> unicode: ...