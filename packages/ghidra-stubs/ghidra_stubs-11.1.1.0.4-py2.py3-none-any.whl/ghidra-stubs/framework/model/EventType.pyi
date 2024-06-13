from typing import overload
import java.lang


class EventType(object):
    """
    Interface for objects that represent event types. This interface has only one method and that
     method exists to facilitate fast checking if an event type is present in a collection of events.
     The value returned from getId() is arbitrary and can change from run to run. Its only purpose
     is to give each event type a unique compact id that can be used as an index into a bit set. It is
     important that implementers of this interface get their id values by calling 
     DomainObjectEventIdGenerator#next() so that all event ids are coordinated and as 
     small as possible.
 
     The preferred implementation of EventType is an enum that enumerates the valid event types
     for any application sub-system. See DomainObjectEvent for an example implementation.
    """









    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getId(self) -> int:
        """
        Returns the unique id assigned to this event type. The value is guaranteed to be constant
         for any given run of the application, but can vary from run to run.
        @return the unique event id assigned to this EventType.
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
    def id(self) -> int: ...