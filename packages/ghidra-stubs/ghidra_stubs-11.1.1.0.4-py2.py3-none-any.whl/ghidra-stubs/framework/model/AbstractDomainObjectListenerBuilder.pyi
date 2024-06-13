from typing import List
from typing import overload
import ghidra.framework.model
import java.lang
import java.util.function
import utility.function


class AbstractDomainObjectListenerBuilder(object):
    """
    Base class for creating a compact and efficient DomainObjectListeners. See
     DomainObjectListenerBuilder for full documentation.
    """






    class AnyBuilder(object):




        def __init__(self, __a0: ghidra.framework.model.AbstractDomainObjectListenerBuilder, __a1: List[ghidra.framework.model.EventType]): ...



        @overload
        def call(self, __a0: java.util.function.Consumer) -> ghidra.framework.model.AbstractDomainObjectListenerBuilder: ...

        @overload
        def call(self, __a0: utility.function.Callback) -> ghidra.framework.model.AbstractDomainObjectListenerBuilder: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        @overload
        def terminate(self, __a0: java.util.function.Consumer) -> ghidra.framework.model.AbstractDomainObjectListenerBuilder: ...

        @overload
        def terminate(self, __a0: utility.function.Callback) -> ghidra.framework.model.AbstractDomainObjectListenerBuilder: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...






    class EachBuilder(object):




        def __init__(self, __a0: ghidra.framework.model.AbstractDomainObjectListenerBuilder, __a1: List[ghidra.framework.model.EventType]): ...



        @overload
        def call(self, __a0: java.util.function.BiConsumer) -> ghidra.framework.model.AbstractDomainObjectListenerBuilder: ...

        @overload
        def call(self, __a0: java.util.function.Consumer) -> ghidra.framework.model.AbstractDomainObjectListenerBuilder: ...

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



    def __init__(self, name: unicode, recordClass: java.lang.Class):
        """
        Creates a builder with the given recordClass as the default record class
        @param name the name of the client class that created this builder
        @param recordClass the class of event records consumers will be using in any calls that
         take a consumer
        """
        ...



    def any(self, eventTypes: List[ghidra.framework.model.EventType]) -> ghidra.framework.model.AbstractDomainObjectListenerBuilder:
        """
        Allows for specifying multiple event types that if the event contains any records with
         and of the given types, then a callback or callback with terminate will be triggered, 
         depending on if the next builder operation is either a call or terminate respectively.
        @param eventTypes the list of events to trigger on
        @return A sub-builder for specifying the call or call with terminate
        """
        ...

    def build(self) -> ghidra.framework.model.DomainObjectListener:
        """
        Builds and returns a new DomainObjectEventHandler
        @return a new DomainObjectEventHandler from this builder
        """
        ...

    def each(self, eventTypes: List[ghidra.framework.model.EventType]) -> ghidra.framework.model.AbstractDomainObjectListenerBuilder:
        """
        Allows for specifying multiple event types that for each record with one of the specified
         types, the follow on consumer will be called.
        @param eventTypes the list of events to trigger on
        @return A sub-builder for specifying the consumer to be used for records with any of
         these types
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getName(self) -> unicode:
        """
        Returns the name that will be associated with the domainObjectListener. this is for
         debugging purposes so that you can tell where this listener came from (since it is
         no longer implemented by the client class)
        @return the name assigned to this builder (and ultimately the listener)
        """
        ...

    def hashCode(self) -> int: ...

    def ignoreWhen(self, supplier: java.util.function.BooleanSupplier) -> int:
        """
        Sets a boolean supplier that can be checked to see if the client is in a state where
         they don't want events to be processed at this time.
        @param supplier the boolean supplier that if returns true, events are not processed
        @return this builder (for chaining)
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def with(self, clazz: java.lang.Class) -> B2:
        """
        Allows for specifying a new record type that any follow on consumers will use for any
         defined "each" handlers.
        @param <R2> the new record type
        @param <B2> the new builder type that expects consumers of the new record type
        @param clazz the class of the new record type
        @return this builder with its consumer record type changed
        """
        ...

    @property
    def name(self) -> unicode: ...