from typing import overload
import ghidra.framework.model
import java.io
import java.lang


class DomainObjectChangeRecord(object, java.io.Serializable):
    """
    Information about a change that was made to a domain object. The record is delivered as part of
     the change notification. The event types correspond to Enums defined in DomainObjectEvent
     and other Enums or objects that implement the EventType interface.
 
 
     Each event record contains the event type and optionally an old value and a new value. The old
     value and new value meaning are determined by the event type.
    """





    @overload
    def __init__(self, eventType: ghidra.framework.model.EventType):
        """
        Construct a new DomainObjectChangeRecord.
        @param eventType the type of event
        """
        ...

    @overload
    def __init__(self, eventType: ghidra.framework.model.EventType, oldValue: object, newValue: object):
        """
        Construct a new DomainObjectChangeRecord.
        @param eventType the type of
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
    def eventType(self) -> ghidra.framework.model.EventType: ...

    @property
    def newValue(self) -> object: ...

    @property
    def oldValue(self) -> object: ...