from typing import List
from typing import overload
import db
import ghidra.framework.data
import ghidra.framework.model
import ghidra.framework.options
import ghidra.util.task
import java.io
import java.lang
import java.util
import utility.function


class DomainObject(object):
    """
    DomainObject is the interface that must be supported by
     data objects that are persistent. DomainObjects maintain an
     association with a DomainFile. A DomainObject that
     has never been saved will have a null DomainFile.
 
     Supports transactions and the ability to undo/redo changes made within a stack of 
     recent transactions.  Each transactions may contain many sub-transactions which
     reflect concurrent changes to the domain object.  If any sub-transaction fails to commit,
     all concurrent sub-transaction changes will be rolled-back. 
 
     NOTE: A transaction must be started in order
     to make any change to this domain object - failure to do so will result in a 
     IOException.
 
     Note: Previously (before 11.1), domain object change event types were defined in this file as
     integer constants. Event ids have since been converted to enum types. The defines in this file  
     have been converted to point to the new enum values to make it easier to convert to this new way  
     and to clearly see how the old values map to the new enums. In future releases, these defines 
     will be removed.
    """

    DO_DOMAIN_FILE_CHANGED: ghidra.framework.model.EventType
    DO_OBJECT_CLOSED: ghidra.framework.model.EventType
    DO_OBJECT_ERROR: ghidra.framework.model.EventType
    DO_OBJECT_RENAMED: ghidra.framework.model.EventType
    DO_OBJECT_RESTORED: ghidra.framework.model.EventType
    DO_OBJECT_SAVED: ghidra.framework.model.EventType
    DO_PROPERTY_CHANGED: ghidra.framework.model.EventType
    undoLock: object







    def addCloseListener(self, listener: ghidra.framework.model.DomainObjectClosedListener) -> None:
        """
        Adds a listener that will be notified when this DomainObject is closed.  This is meant
         for clients to have a chance to cleanup, such as reference removal.
        @param listener the reference to add
        """
        ...

    def addConsumer(self, consumer: object) -> bool:
        """
        Adds the given object as a consumer.  The release method must be invoked
         with this same consumer instance when this domain object is no longer in-use.
        @param consumer domain object consumer
        @return false if this domain object has already been closed
        """
        ...

    def addDomainFileListener(self, listener: ghidra.framework.data.DomainObjectFileListener) -> None:
        """
        Adds a listener that will be notified when this DomainFile associated with this
         DomainObject changes, such as when a 'Save As' action occurs. Unlike DomainObject events,
         these notifications are not buffered and happen immediately when the DomainFile is changed.
        @param listener the listener to be notified when the associated DomainFile changes
        """
        ...

    def addListener(self, dol: ghidra.framework.model.DomainObjectListener) -> None:
        """
        Adds a listener for this object.
        @param dol listener notified when any change occurs to this domain object
        """
        ...

    def addSynchronizedDomainObject(self, domainObj: ghidra.framework.model.DomainObject) -> None:
        """
        Synchronize the specified domain object with this domain object
         using a shared transaction manager.  If either or both is already shared, 
         a transition to a single shared transaction manager will be 
         performed.
        @param domainObj the domain object
        @throws LockException if lock or open transaction is active on either
         this or the specified domain object
        """
        ...

    def addTransactionListener(self, listener: ghidra.framework.model.TransactionListener) -> None:
        """
        Adds the given transaction listener to this domain object
        @param listener the new transaction listener to add
        """
        ...

    def canLock(self) -> bool:
        """
        Returns true if a modification lock can be obtained on this
         domain object.  Care should be taken with using this method since
         this will not prevent another thread from modifying the domain object.
        @return true if can lock
        """
        ...

    def canRedo(self) -> bool:
        """
        Returns true if there is a later state to "redo" to.
        """
        ...

    def canSave(self) -> bool:
        """
        Returns true if this object can be saved; a read-only file cannot be saved.
        @return true if this object can be saved
        """
        ...

    def canUndo(self) -> bool:
        """
        Returns true if there is a previous state to "undo" to.
        """
        ...

    def clearUndo(self) -> None:
        """
        Clear all undoable/redoable transactions
        """
        ...

    def createPrivateEventQueue(self, listener: ghidra.framework.model.DomainObjectListener, maxDelay: int) -> ghidra.framework.model.EventQueueID:
        """
        Creates a private event queue that can be flushed independently from the main event queue.
        @param listener the listener to be notified of domain object events.
        @param maxDelay the time interval (in milliseconds) used to buffer events.
        @return a unique identifier for this private queue.
        """
        ...

    def endTransaction(self, transactionID: int, commit: bool) -> None:
        """
        Terminate the specified transaction for this domain object.
        @param transactionID transaction ID obtained from startTransaction method
        @param commit if true the changes made in this transaction will be marked for commit,
         if false this and any concurrent transaction will be rolled-back.
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def flushEvents(self) -> None:
        """
        Makes sure all pending domainEvents have been sent.
        """
        ...

    def flushPrivateEventQueue(self, id: ghidra.framework.model.EventQueueID) -> None:
        """
        Flush events from the specified event queue.
        @param id the id specifying the event queue to be flushed.
        """
        ...

    def forceLock(self, rollback: bool, reason: unicode) -> None:
        """
        Force transaction lock and terminate current transaction.
        @param rollback true if rollback of non-commited changes should occurs, false if commit
         should be done.  NOTE: it can be potentially detrimental to commit an incomplete transaction
         which should be avoided.
        @param reason very short reason for requesting lock
        """
        ...

    def getAllRedoNames(self) -> List[unicode]:
        """
        Returns a list of the names of all current redo transactions
        @return a list of the names of all current redo transactions
        """
        ...

    def getAllUndoNames(self) -> List[unicode]:
        """
        Returns a list of the names of all current undo transactions
        @return a list of the names of all current undo transactions
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getConsumerList(self) -> List[object]:
        """
        Returns the list of consumers on this domainObject
        @return the list of consumers.
        """
        ...

    def getCurrentTransactionInfo(self) -> ghidra.framework.model.TransactionInfo:
        """
        Returns the current transaction info
        @return the current transaction info
        """
        ...

    def getDescription(self) -> unicode:
        """
        Returns a word or short phrase that best describes or categorizes
         the object in terms that a user will understand.
        @return the description
        """
        ...

    def getDomainFile(self) -> ghidra.framework.model.DomainFile:
        """
        Get the domain file for this domain object.
        @return the associated domain file
        """
        ...

    def getMetadata(self) -> java.util.Map:
        """
        Returns a map containing all the stored metadata associated with this domain object.  The map
         contains key,value pairs and are ordered by their insertion order.
        @return a map containing all the stored metadata associated with this domain object.
        """
        ...

    def getModificationNumber(self) -> long:
        """
        Returns a long value that gets incremented every time a change, undo, or redo takes place.
         Useful for implementing a lazy caching system.
        @return a long value that is incremented for every change to the program.
        """
        ...

    def getName(self) -> unicode:
        """
        Get the name of this domain object.
        @return the name
        """
        ...

    def getOptions(self, propertyListName: unicode) -> ghidra.framework.options.Options:
        """
        Get the property list for the given name.
        @param propertyListName name of property list
        @return the options
        """
        ...

    def getOptionsNames(self) -> List[unicode]:
        """
        Returns all properties lists contained by this domain object.
        @return all property lists contained by this domain object.
        """
        ...

    def getRedoName(self) -> unicode:
        """
        Returns a description of the change that would be "redone".
        @return a description of the change that would be "redone".
        """
        ...

    def getSynchronizedDomainObjects(self) -> List[ghidra.framework.model.DomainObject]:
        """
        Return array of all domain objects synchronized with a 
         shared transaction manager.
        @return returns array of synchronized domain objects or
         null if this domain object is not synchronized with others.
        """
        ...

    def getUndoName(self) -> unicode:
        """
        Returns a description of the change that would be "undone".
        @return a description of the change that would be "undone".
        """
        ...

    def hasExclusiveAccess(self) -> bool:
        """
        Returns true if the user has exclusive access to the domain object.  Exclusive access means
         either the object is not shared or the user has an exclusive checkout on the object.
        @return true if has exclusive access
        """
        ...

    def hasTerminatedTransaction(self) -> bool:
        """
        Returns true if the last transaction was terminated from the action that started it.
        @return true if the last transaction was terminated from the action that started it.
        """
        ...

    def hashCode(self) -> int: ...

    def isChangeable(self) -> bool:
        """
        Returns true if changes are permitted.
        @return true if changes are permitted.
        """
        ...

    def isChanged(self) -> bool:
        """
        Returns whether the object has changed.
        @return whether the object has changed.
        """
        ...

    def isClosed(self) -> bool:
        """
        Returns true if this domain object has been closed as a result of the last release
        @return true if closed
        """
        ...

    def isLocked(self) -> bool:
        """
        Returns true if the domain object currently has a modification lock enabled.
        @return true if locked
        """
        ...

    def isSendingEvents(self) -> bool:
        """
        Returns true if this object is sending out events as it is changed.  The default is
         true.  You can change this value by calling {@link #setEventsEnabled(boolean)}.
        @return true if sending events
        @see #setEventsEnabled(boolean)
        """
        ...

    def isTemporary(self) -> bool:
        """
        Returns true if this object has been marked as Temporary.
        @return true if this object has been marked as Temporary.
        """
        ...

    def isUsedBy(self, consumer: object) -> bool:
        """
        Returns true if the given consumer is using (has open) this domain object.
        @param consumer the object to test to see if it is a consumer of this domain object.
        @return true if the given consumer is using (has open) this domain object;
        """
        ...

    def lock(self, reason: unicode) -> bool:
        """
        Attempt to obtain a modification lock on the domain object.  Multiple locks may be granted
         on this domain object, although all lock owners must release their lock in a timely fashion.
        @param reason very short reason for requesting lock
        @return true if lock obtained successfully, else false which indicates that a modification
         is in process.
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def openTransaction(self, description: unicode) -> db.Transaction:
        """
        Open new transaction.  This should generally be done with a try-with-resources block:
         <pre>
         try (Transaction tx = dobj.openTransaction(description)) {
         	// ... Do something
         }
         </pre>
        @param description a short description of the changes to be made.
        @return transaction object
        @throws IllegalStateException if this {@link DomainObject} has already been closed.
        """
        ...

    def redo(self) -> None:
        """
        Returns to a latter state that exists because of an undo.  Normally, this
         will cause the current state to appear on the "undo" stack.  This method
         will do nothing if there are no latter states to "redo".
        @throws IOException if an IO error occurs
        """
        ...

    def release(self, consumer: object) -> None:
        """
        Notify the domain object that the specified consumer is no longer using it.
         When the last consumer invokes this method, the domain object will be closed
         and will become invalid.
        @param consumer the consumer (e.g., tool, plugin, etc) of the domain object
         previously established with the addConsumer method.
        """
        ...

    def releaseSynchronizedDomainObject(self) -> None:
        """
        Remove this domain object from a shared transaction manager.  If
         this object has not been synchronized with others via a shared
         transaction manager, this method will have no affect.
        @throws LockException if lock or open transaction is active
        """
        ...

    def removeCloseListener(self, listener: ghidra.framework.model.DomainObjectClosedListener) -> None:
        """
        Removes the given close listener.
        @param listener the listener to remove.
        """
        ...

    def removeDomainFileListener(self, listener: ghidra.framework.data.DomainObjectFileListener) -> None:
        """
        Removes the given DomainObjectFileListener listener.
        @param listener the listener to remove.
        """
        ...

    def removeListener(self, dol: ghidra.framework.model.DomainObjectListener) -> None:
        """
        Remove the listener for this object.
        @param dol listener
        """
        ...

    def removePrivateEventQueue(self, id: ghidra.framework.model.EventQueueID) -> bool:
        """
        Removes the specified private event queue
        @param id the id of the queue to remove.
        @return true if the id represents a valid queue that was removed.
        """
        ...

    def removeTransactionListener(self, listener: ghidra.framework.model.TransactionListener) -> None:
        """
        Removes the given transaction listener from this domain object.
        @param listener the transaction listener to remove
        """
        ...

    def save(self, comment: unicode, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Saves changes to the DomainFile.
        @param comment comment used for new version
        @param monitor monitor that shows the progress of the save
        @throws IOException thrown if there was an error accessing this
         domain object
        @throws ReadOnlyException thrown if this DomainObject is read only
         and cannot be saved
        @throws CancelledException thrown if the user canceled the save
         operation
        """
        ...

    def saveToPackedFile(self, outputFile: java.io.File, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Saves (i.e., serializes) the current content to a packed file.
        @param outputFile packed output file
        @param monitor progress monitor
        @throws IOException if an exception occurs
        @throws CancelledException if the user cancels
        @throws UnsupportedOperationException if not supported by object implementation
        """
        ...

    def setEventsEnabled(self, enabled: bool) -> None:
        """
        If true, domain object change events are sent. If false, no events are sent.
         <p>
         <b>
         NOTE: disabling events could cause plugins to be out of sync!
         </b>
         <p>
         NOTE: when re-enabling events, an event will be sent to the system to signal that
               every listener should update.
        @param enabled true means to enable events
        """
        ...

    def setName(self, name: unicode) -> None:
        """
        Set the name for this domain object.
        @param name object name
        """
        ...

    def setTemporary(self, state: bool) -> None:
        """
        Set the temporary state of this object.
         If this object is temporary, the isChanged() method will
         always return false.  The default temporary state is false.
        @param state if true object is marked as temporary
        """
        ...

    @overload
    def startTransaction(self, description: unicode) -> int:
        """
        Start a new transaction in order to make changes to this domain object.
         All changes must be made in the context of a transaction. 
         If a transaction is already in progress, a sub-transaction 
         of the current transaction will be returned.
        @param description brief description of transaction
        @return transaction ID
        @throws DomainObjectLockedException the domain object is currently locked
        @throws TerminatedTransactionException an existing transaction which has not yet ended was terminated early.
         Sub-transactions are not permitted until the terminated transaction ends.
        """
        ...

    @overload
    def startTransaction(self, description: unicode, listener: ghidra.framework.model.AbortedTransactionListener) -> int:
        """
        Start a new transaction in order to make changes to this domain object.
         All changes must be made in the context of a transaction. 
         If a transaction is already in progress, a sub-transaction 
         of the current transaction will be returned.
        @param description brief description of transaction
        @param listener listener to be notified if the transaction is aborted.
        @return transaction ID
        @throws DomainObjectLockedException the domain object is currently locked
        @throws TerminatedTransactionException an existing transaction which has not yet ended was terminated early.
         Sub-transactions are not permitted until the terminated transaction ends.
        """
        ...

    def toString(self) -> unicode: ...

    def undo(self) -> None:
        """
        Returns to the previous state.  Normally, this will cause the current state
         to appear on the "redo" stack.  This method will do nothing if there are
         no previous states to "undo".
        @throws IOException if an IO error occurs
        """
        ...

    def unlock(self) -> None:
        """
        Release a modification lock previously granted with the lock method.
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @overload
    def withTransaction(self, description: unicode, callback: utility.function.ExceptionalCallback) -> None:
        """
        Performs the given callback inside of a transaction.  Use this method in place of the more
         verbose try/catch/finally semantics.
         <p>
         <pre>
         program.withTransaction("My Description", () -> {
         	// ... Do something
         });
         </pre>
 
         <p>
         Note: the transaction created by this method will always be committed when the call is 
         finished.  If you need the ability to abort transactions, then you need to use the other 
         methods on this interface.
        @param description brief description of transaction
        @param callback the callback that will be called inside of a transaction
        @throws E any exception that may be thrown in the given callback
        """
        ...

    @overload
    def withTransaction(self, description: unicode, supplier: utility.function.ExceptionalSupplier) -> object:
        """
        Calls the given supplier inside of a transaction.  Use this method in place of the more
         verbose try/catch/finally semantics.
         <p>
         <pre>
         program.withTransaction("My Description", () -> {
         	// ... Do something
         	return result;
         });
         </pre>
         <p>
         If you do not need to supply a result, then use 
         {@link #withTransaction(String, ExceptionalCallback)} instead.
        @param <E> the exception that may be thrown from this method
        @param <T> the type of result returned by the supplier
        @param description brief description of transaction
        @param supplier the supplier that will be called inside of a transaction
        @return the result returned by the supplier
        @throws E any exception that may be thrown in the given callback
        """
        ...

    @property
    def allRedoNames(self) -> List[object]: ...

    @property
    def allUndoNames(self) -> List[object]: ...

    @property
    def changeable(self) -> bool: ...

    @property
    def changed(self) -> bool: ...

    @property
    def closed(self) -> bool: ...

    @property
    def consumerList(self) -> List[object]: ...

    @property
    def currentTransactionInfo(self) -> ghidra.framework.model.TransactionInfo: ...

    @property
    def description(self) -> unicode: ...

    @property
    def domainFile(self) -> ghidra.framework.model.DomainFile: ...

    @property
    def eventsEnabled(self) -> None: ...  # No getter available.

    @eventsEnabled.setter
    def eventsEnabled(self, value: bool) -> None: ...

    @property
    def locked(self) -> bool: ...

    @property
    def metadata(self) -> java.util.Map: ...

    @property
    def modificationNumber(self) -> long: ...

    @property
    def name(self) -> unicode: ...

    @name.setter
    def name(self, value: unicode) -> None: ...

    @property
    def optionsNames(self) -> List[object]: ...

    @property
    def redoName(self) -> unicode: ...

    @property
    def sendingEvents(self) -> bool: ...

    @property
    def synchronizedDomainObjects(self) -> List[ghidra.framework.model.DomainObject]: ...

    @property
    def temporary(self) -> bool: ...

    @temporary.setter
    def temporary(self, value: bool) -> None: ...

    @property
    def undoName(self) -> unicode: ...