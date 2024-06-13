from typing import List
from typing import overload
import ghidra.framework.model
import java.lang
import java.util.function


class DomainObjectListenerBuilder(ghidra.framework.model.AbstractDomainObjectListenerBuilder):
    """
    Builder for creating a compact and efficient DomainObjectListener for 
     DomainObjectChangedEvents
 
     There are three basic ways to process DomainObjectChangeRecords within a 
     DomainObjectChangedEvent. 
     The first way is to look for the event to contain one or more
     records of a certain type, and if it is there, do some major refresh operation, and ignore
     the remaining event records. This is can be handled with an #any(EventType...),  
     followed by a AnyBuilder#terminate(Callback) or AnyBuilder#terminate(Consumer) 
     if you want the event.
 
 
     new DomainObjectListenerBuilder()
    	.any(DomainObjectEvent.RESTORED).call(() -> refreshAll())
    	.build();
 
 
    or if you need the event, you can use a consumer

  
     new DomainObjectListenerBuilder()
    	.any(DomainObjectEvent.RESTORED).call(e -> refreshAll(e))
    	.build();
 
 
     The second way is to just test for presence of one or more records of a certain type, and if
     any of those types exist is the event, call a method. In this case you don't need to know the 
     details of the record, only that one of the  given events was fired. This can be handled using 
     the  #any(EventType...), followed by a  call to AnyBuilder#call(Callback) or
     AnyBuilder#call(Consumer)
 
 
     new DomainObjectListenerBuilder()
    	.onAny(ProgramEvent.FUNCTION_CHANGED).call(() -> refreshFunctions())
    	.build();
 
    or if you need the event, you can use a consumer
 

     new DomainObjectListenerBuilder()
    	.onAny(ProgramEvent.FUNCTION_CHANGED).call(e -> refreshFunctions(e))
    	.build();
 
 
     And finally, the third way is where you have to perform some processing on each record of a 
     certain type. This can be done using the the #each(EventType...), followed by the
     EachBuilder#call(Consumer) if you just want the record, or 
     EachBuilder#call(BiConsumer) if you want the record and the event.
 
     By default, the consumer for the "each" case is typed on DomainObjectChangeRecord. But that
     can be changed by calling #with(Class). Once this is called the builder
     will require that all consumers being passed in will now be typed on that record
     class. 
 
 
     new DomainObjectListenerBuilder()
    	.each(DomainObjectEvent.PROPERTY_CHANGED).call(r -> processPropertyChanged(r))
    	.withRecord(ProgramChangeRecord.class)
    	.each(ProgramEvent.SYMBOL_RENANED).call(r -> symbolRenamed(r)
    	.build();

     private void processPropertyChanged(DomainObjectChangeRecord record) {
     		...
     }
     private void symbolRenamed(ProgramChangeRecord record) {
     		...
     }
 
 
     or if you also need the event (to get the domainObject that is the event source)
 
 
       new DomainObjectListenerBuilder()
    	.each(DomainObjectEvent.PROPERTY_CHANGED).call((e, r) -> processPropertyChanged(e, r))
    	.withRecord(ProgramChangeRecord.class)
    	.each(ProgramEvent.SYMBOL_RENANED).call((e, r) -> symbolRenamed(e, r)
    	.build();

     private void propertyChanged(DomainObjectChangedEvent e, DomainObjectChangeRecord record) {
     	    Program p = (Program)e.getSource().
     		...
     }
     private void symbolRenamed(DomainObjectChangedEvent e, ProgramChangeRecord record) {
     	    Program p = (Program)e.getSource().
     	    ...
     }
 
    """





    def __init__(self, creator: object):
        """
        Constructs a new builder
        @param creator the object that created this builder (usually, just pass in "this"). This
         will help with debugging event processing
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

