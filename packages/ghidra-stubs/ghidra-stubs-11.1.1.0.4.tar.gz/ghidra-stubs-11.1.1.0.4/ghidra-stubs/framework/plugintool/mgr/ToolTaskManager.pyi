from typing import overload
import ghidra.framework.cmd
import ghidra.framework.model
import ghidra.framework.plugintool.mgr
import ghidra.util.task
import java.lang
import java.util.function
import javax.swing


class ToolTaskManager(object, java.lang.Runnable):
    """
    Manages a queue of background tasks that execute commands.
    """





    def __init__(self, tool: ghidra.framework.plugintool.PluginTool):
        """
        Construct a new ToolTaskManager.
        @param tool tool associated with this ToolTaskManager
        """
        ...



    def cancelCurrentTask(self) -> None:
        """
        Cancel the current task.
        """
        ...

    def clearQueuedCommands(self, obj: ghidra.framework.model.DomainObject) -> None:
        """
        Clear the queue of scheduled commands.
        @param obj domain object
        """
        ...

    @overload
    def clearTasks(self) -> None:
        """
        Clear the list of tasks.
        """
        ...

    @overload
    def clearTasks(self, obj: ghidra.framework.model.DomainObject) -> None:
        """
        Clear all tasks associated with specified domain object.
        @param obj domain object
        """
        ...

    def dispose(self) -> None:
        """
        Clear list of tasks and queue of scheduled commands.
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    @overload
    def execute(self, __a0: ghidra.framework.cmd.Command, __a1: ghidra.framework.model.DomainObject) -> bool: ...

    @overload
    def execute(self, __a0: unicode, __a1: ghidra.framework.model.DomainObject, __a2: java.util.function.Function) -> bool: ...

    def executeCommand(self, __a0: ghidra.framework.cmd.BackgroundCommand, __a1: ghidra.framework.model.DomainObject) -> None: ...

    def getClass(self) -> java.lang.Class: ...

    def getMonitorComponent(self) -> javax.swing.JComponent:
        """
        Get the monitor component that shows progress and has a cancel button.
        @return the monitor component
        """
        ...

    def getTaskThreadGroup(self) -> java.lang.ThreadGroup:
        """
        Returns the thread group associated with all background tasks run by this
         manager and their instantiated threads.
        @return task thread group
        """
        ...

    def hasTasksForDomainObject(self, domainObject: ghidra.framework.model.DomainObject) -> bool: ...

    def hashCode(self) -> int: ...

    def isBusy(self) -> bool:
        """
        Return true if a task is executing
        @return true if a task is executing
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def run(self) -> None: ...

    def scheduleFollowOnCommand(self, __a0: ghidra.framework.cmd.BackgroundCommand, __a1: ghidra.framework.model.DomainObject) -> None: ...

    def stop(self, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Cancel the currently running task and clear all commands that are scheduled to run. Block
         until the currently running task ends.
        @param monitor a monitor to cancel waiting for the task to finish
        """
        ...

    def taskCompleted(self, __a0: ghidra.framework.model.DomainObject, __a1: ghidra.framework.plugintool.mgr.BackgroundCommandTask, __a2: ghidra.util.task.TaskMonitor) -> None: ...

    def taskFailed(self, __a0: ghidra.framework.model.DomainObject, __a1: ghidra.framework.cmd.BackgroundCommand, __a2: ghidra.util.task.TaskMonitor) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def busy(self) -> bool: ...

    @property
    def monitorComponent(self) -> javax.swing.JComponent: ...

    @property
    def taskThreadGroup(self) -> java.lang.ThreadGroup: ...