from typing import overload
import ghidra.framework.protocol.ghidra
import ghidra.util.task
import java.lang
import java.net


class GhidraURLQuery(object):
    """
    GhidraURLQuery performs remote Ghidra repository and read-only local project
     queries for processing either a DomainFile or DomainFolder that a 
     Ghidra URL may reference.
    """





    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def queryRepositoryUrl(ghidraUrl: java.net.URL, readOnly: bool, resultHandler: ghidra.framework.protocol.ghidra.GhidraURLResultHandler, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Perform query using specified GhidraURL and process result.
         Both local project and remote repository URLs are supported.
         This method is intended to be invoked from within a {@link Task} or for headless operations.
        @param ghidraUrl local or remote Ghidra URL
        @param readOnly allows update/commit (false) or read-only (true) access.
        @param resultHandler query result handler
        @param monitor task monitor
        @throws IOException if an IO error occurs which was re-thrown by {@code resultHandler}
        @throws CancelledException if task is cancelled
        """
        ...

    @staticmethod
    def queryUrl(ghidraUrl: java.net.URL, resultHandler: ghidra.framework.protocol.ghidra.GhidraURLResultHandler, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Perform read-only query using specified GhidraURL and process result.
         Both local project and remote repository URLs are supported.
         This method is intended to be invoked from within a {@link Task} or for headless operations.
        @param ghidraUrl local or remote Ghidra URL
        @param resultHandler query result handler
        @param monitor task monitor
        @throws IOException if an IO error occurs which was re-thrown by {@code resultHandler}
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

