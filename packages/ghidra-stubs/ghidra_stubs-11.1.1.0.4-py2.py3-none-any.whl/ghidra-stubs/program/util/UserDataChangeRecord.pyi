from typing import overload
import ghidra.framework.model
import java.lang


class UserDataChangeRecord(ghidra.framework.model.DomainObjectChangeRecord):




    @overload
    def __init__(self, propertyName: unicode):
        """
        Constructor for change record for removing a range of properties.
        @param propertyName name of the property
        """
        ...

    @overload
    def __init__(self, propertyName: unicode, oldValue: object, newValue: object):
        """
        Constructor
        @param propertyName name of the property
        @param oldValue old value
        @param newValue new value
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

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

    def getOldValue(self) -> object:
        """
        Return the old value for this event or null if not applicable.
        @return the old value or null if not applicable
        """
        ...

    def getPropertyName(self) -> unicode:
        """
        Get the name of the property being changed.
        @return the name of the property being changed.
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