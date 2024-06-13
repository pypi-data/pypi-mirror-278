from typing import overload
import ghidra.framework.model
import ghidra.framework.protocol.ghidra
import ghidra.util.task
import java.io
import java.lang
import java.net


class GhidraURLResultHandlerAdapter(object, ghidra.framework.protocol.ghidra.GhidraURLResultHandler):
    """
    GhidraURLResultHandlerAdapter provides a basic result handler for 
     GhidraURLQuery.  All uses of this adapter should override one or
     both of the processing methods #processResult(DomainFile, URL, TaskMonitor)
     and #processResult(DomainFolder, URL, TaskMonitor).  For any process method
     not overriden the default behavior is reporting Unsupported Content.
    """





    @overload
    def __init__(self):
        """
        Construct adapter.  If {@link #handleError(String, String, URL, IOException)}
         is not overriden all errors are reported via 
         {@link Msg#showError(Object, java.awt.Component, String, Object)}.
        """
        ...

    @overload
    def __init__(self, throwErrorByDefault: bool):
        """
        Construct adapter with preferred error handling.  There is no need to use this constructor
         if {@link #handleError(String, String, URL, IOException)} is override.
        @param throwErrorByDefault if true all errors will be thrown as an {@link IOException},
         otherwise error is reported via {@link Msg#showError(Object, java.awt.Component, String, Object)}.
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def handleError(self, title: unicode, message: unicode, url: java.net.URL, cause: java.io.IOException) -> None: ...

    def handleUnauthorizedAccess(self, __a0: java.net.URL) -> None: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @overload
    def processResult(self, domainFile: ghidra.framework.model.DomainFile, url: java.net.URL, monitor: ghidra.util.task.TaskMonitor) -> None: ...

    @overload
    def processResult(self, domainFolder: ghidra.framework.model.DomainFolder, url: java.net.URL, monitor: ghidra.util.task.TaskMonitor) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

