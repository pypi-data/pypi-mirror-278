from typing import overload
import ghidra.debug.api.progress
import ghidra.util.task
import java.lang
import java.util
import java.util.concurrent
import java.util.function


class ProgressService(object):








    def addProgressListener(self, __a0: ghidra.debug.api.progress.ProgressListener) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    @overload
    def execute(self, __a0: ghidra.util.task.Task) -> java.util.concurrent.CompletableFuture: ...

    @overload
    def execute(self, __a0: bool, __a1: bool, __a2: bool, __a3: java.util.function.Function) -> java.util.concurrent.CompletableFuture: ...

    def getAllMonitors(self) -> java.util.Collection: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def publishTask(self) -> ghidra.debug.api.progress.CloseableTaskMonitor: ...

    def removeProgressListener(self, __a0: ghidra.debug.api.progress.ProgressListener) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def allMonitors(self) -> java.util.Collection: ...