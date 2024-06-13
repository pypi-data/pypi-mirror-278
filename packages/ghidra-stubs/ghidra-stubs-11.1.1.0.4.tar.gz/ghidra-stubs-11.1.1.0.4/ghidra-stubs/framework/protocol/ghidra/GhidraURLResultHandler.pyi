from typing import overload
import ghidra.framework.model
import ghidra.util.task
import java.io
import java.lang
import java.net


class GhidraURLResultHandler(object):








    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def handleError(self, title: unicode, message: unicode, url: java.net.URL, cause: java.io.IOException) -> None:
        """
        Handle error which occurs during query operation.
        @param title error title
        @param message error detail
        @param url URL which was used for query
        @param cause cause of error (may be null)
        @throws IOException may be thrown if handler decides to propogate error
        """
        ...

    def handleUnauthorizedAccess(self, url: java.net.URL) -> None:
        """
        Handle authorization error. 
         This condition is generally logged and user notified via GUI during connection processing.
         This method does not do anything by default but is provided to flag failure if needed since
         {@link #handleError(String, String, URL, IOException)} will not be invoked.
        @param url connection URL
        @throws IOException may be thrown if handler decides to propogate error
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    def processResult(self, domainFile: ghidra.framework.model.DomainFile, url: java.net.URL, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Process the specified {@code domainFile} query result. 
         Dissemination of the {@code domainFile} instance should be restricted and any use of it 
         completed before the call to this method returns.  Upon return from this method call the 
         underlying connection will be closed and at which time the {@code domainFile} instance 
         will become invalid.
        @param domainFile {@link DomainFile} to which the URL refers.
        @param url URL which was used to retrieve the specified {@code domainFile}
        @param monitor task monitor
        @throws IOException if an IO error occurs
        @throws CancelledException if task is cancelled
        """
        ...

    @overload
    def processResult(self, domainFolder: ghidra.framework.model.DomainFolder, url: java.net.URL, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Process the specified {@code domainFolder} query result.
         Dissemination of the {@code domainFolder} instance should be restricted and any use of it 
         completed before the call to this method returns.  Upon return from this method call the 
         underlying connection will be closed and at which time the {@code domainFolder} instance 
         will become invalid.
        @param domainFolder {@link DomainFolder} to which the URL refers.
        @param url URL which was used to retrieve the specified {@code domainFolder}
        @param monitor task monitor
        @throws IOException if an IO error occurs
        @throws CancelledException if task is cancelled
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

