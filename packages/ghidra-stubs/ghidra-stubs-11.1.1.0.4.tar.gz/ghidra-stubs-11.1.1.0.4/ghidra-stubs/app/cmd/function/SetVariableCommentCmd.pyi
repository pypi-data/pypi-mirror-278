from typing import overload
import ghidra.framework.cmd
import ghidra.framework.model
import ghidra.program.model.listing
import java.lang


class SetVariableCommentCmd(object, ghidra.framework.cmd.Command):
    """
    Command to set the comment on a function varible.
    """





    def __init__(self, var: ghidra.program.model.listing.Variable, newComment: unicode):
        """
        Constructs a new command for setting the comment on a function variable.
        @param var the variable on which to set the comment.
        @param newComment the comment string to set on the specified variable.
        """
        ...



    @overload
    def applyTo(self, program: ghidra.program.model.listing.Program) -> bool: ...

    @overload
    def applyTo(self, __a0: ghidra.framework.model.DomainObject) -> bool: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getName(self) -> unicode: ...

    def getStatusMsg(self) -> unicode: ...

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
    def name(self) -> unicode: ...

    @property
    def statusMsg(self) -> unicode: ...