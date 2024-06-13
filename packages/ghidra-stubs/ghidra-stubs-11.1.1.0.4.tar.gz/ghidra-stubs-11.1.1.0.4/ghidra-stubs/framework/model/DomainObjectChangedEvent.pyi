from typing import Iterator
from typing import List
from typing import overload
import ghidra.framework.model
import java.lang
import java.util
import java.util.function


class DomainObjectChangedEvent(java.util.EventObject, java.lang.Iterable):
    """
    An event indicating a DomainObject has changed.  This event is actually
     a list of DomainObjectChangeRecords.
  
     NOTE: This object is TRANSIENT - it is only valid during the life of calls
     to all the DomainObjectChangeListeners.  Listeners who need to retain
     any of this event information past the listener call should save the 
     DomainObjectChangeRecords, which will remain valid always.
    """





    def __init__(self, __a0: ghidra.framework.model.DomainObject, __a1: List[object]): ...

    def __iter__(self): ...

    @overload
    def contains(self, types: List[ghidra.framework.model.EventType]) -> bool:
        """
        Returns true if this event contains a record with any of the given event types.
        @param types the event types to check for
        @return true if this event contains a record with any of the given event types
        """
        ...

    @overload
    def contains(self, eventType: ghidra.framework.model.EventType) -> bool:
        """
        Returns true if this event contains a record with the given event type
        @param eventType the event type to check
        @return the number of change records contained within this event.
        """
        ...

    def containsEvent(self, eventType: ghidra.framework.model.EventType) -> bool:
        """
        Returns true if this event contains a record with the given event type.
        @param eventType the event type to check
        @return the number of change records contained within this event.
        @deprecated use {@link #contains(EventType)} instead. This is here to help
         transition older code from using integer constants for even types to the new enum way
         that uses enums instead.
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def findFirst(self, eventType: ghidra.framework.model.EventType) -> ghidra.framework.model.DomainObjectChangeRecord:
        """
        Finds the first record with the given event type.
        @param eventType the event type to search for
        @return the first record with the given event type
        """
        ...

    @overload
    def forEach(self, __a0: java.util.function.Consumer) -> None: ...

    @overload
    def forEach(self, type: ghidra.framework.model.EventType, consumer: java.util.function.Consumer) -> None:
        """
        Loops over all records in this event and calls the consumer for each record that matches
         the given type.
        @param type the event type to apply the consumer
        @param consumer the consumer to call for each record of the given type
        """
        ...

    def getChangeRecord(self, i: int) -> ghidra.framework.model.DomainObjectChangeRecord:
        """
        Get the specified change record within this event.
        @param i change record number
        @return change record
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getSource(self) -> object: ...

    def hashCode(self) -> int: ...

    def iterator(self) -> Iterator[ghidra.framework.model.DomainObjectChangeRecord]:
        """
        Returns iterator over all sub-events
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def numRecords(self) -> int:
        """
        Return the number of change records contained within this event.
        @return the number of change records contained within this event
        """
        ...

    def spliterator(self) -> java.util.Spliterator: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

