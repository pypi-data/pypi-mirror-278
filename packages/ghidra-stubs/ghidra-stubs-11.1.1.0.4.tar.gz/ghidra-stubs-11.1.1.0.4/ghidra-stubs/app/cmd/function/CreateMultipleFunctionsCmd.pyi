from typing import overload
import ghidra.framework.cmd
import ghidra.framework.model
import ghidra.framework.plugintool
import ghidra.program.model.listing
import ghidra.util.task
import java.lang


class CreateMultipleFunctionsCmd(ghidra.framework.cmd.BackgroundCommand):
    """
    Command for Creating multiple functions from a selection.
     This tries to create functions by working from the minimum address to the maximum address in
     the selection. Any addresses in the selection that are already in existing functions are
     discarded. Every time a function is created, all the other addresses for that function are
     also discarded.
    """





    def __init__(self, selection: ghidra.program.model.address.AddressSetView, source: ghidra.program.model.symbol.SourceType): ...



    @overload
    def applyTo(self, __a0: ghidra.framework.model.DomainObject) -> bool: ...

    @overload
    def applyTo(self, program: ghidra.program.model.listing.Program, monitor: ghidra.util.task.TaskMonitor) -> bool: ...

    @overload
    def applyTo(self, __a0: ghidra.framework.model.DomainObject, __a1: ghidra.util.task.TaskMonitor) -> bool: ...

    def canCancel(self) -> bool:
        """
        Check if the command can be canceled.
        @return true if this command can be canceled
        """
        ...

    def dispose(self) -> None:
        """
        Called when this command is going to be removed/canceled without
         running it.  This gives the command the opportunity to free any
         temporary resources it has hold of.
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getName(self) -> unicode: ...

    def getStatusMsg(self) -> unicode: ...

    def hasProgress(self) -> bool:
        """
        Check if the command provides progress information.
        @return true if the command shows progress information
        """
        ...

    def hashCode(self) -> int: ...

    def isModal(self) -> bool:
        """
        Check if the command requires the monitor to be modal.  No other
         command should be allowed, and the GUI will be locked.
        @return true if no other operation should be going on while this
         command is in progress.
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def run(self, __a0: ghidra.framework.plugintool.PluginTool, __a1: ghidra.framework.model.DomainObject) -> None: ...

    def taskCompleted(self) -> None:
        """
        Called when the task monitor is completely done with indicating progress.
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

